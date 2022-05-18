# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .models import Weather
from datetime import date
from django.utils import timezone


@login_required
def profile(request):
    if request.method == 'POST':
        uc_form = UserUpdateForm(request.POST, instance=request.user)
        pc_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if uc_form.is_valid() and pc_form.is_valid():
            uc_form.save()
            pc_form.save()
            mes_suc = _('Your account has been updated!')
            messages.success(request, mes_suc)
            return redirect('profile')
    else:
        uc_form = UserUpdateForm(instance=request.user)
        pc_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'uc_form': uc_form,
        'pc_form': pc_form,
    }
    return render(request, 'users/profile.html', context)


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/User_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        user = self.get_object()
        if self.request.user.id == user.id:
            return True
        return False


@login_required
def weather(request):
    if not request.user.profile.weather:
        mes = _('Weather is not enabled in your profile.')
        messages.warning(request, mes)
        return redirect('profile')

    weathers = Weather.objects.get(user=request.user)
    if weathers.wdate0 == date.today():
        sync = True
    else:
        sync = False
        
    if weathers.alert_end > timezone.now():
        alert = True
    else:
        alert = False

    unites = request.user.profile.unites
    if unites == '1':
        u1, u2 = '°C', 'm/s'
    elif unites == '2':
        u1, u2 = '°F', 'miles/hour'
    elif unites == '3':
        u1, u2 = '°K', 'm/s'

    context = {'title': _('Weather'), 'weathers': weathers, 'sync': sync, 'u1': u1, 'u2': u2, 'alert': alert}
    return render(request, 'users/weather.html', context)
