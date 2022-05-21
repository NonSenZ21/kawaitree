from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.utils import timezone
from .models import Weather
from core.models import Photo, Tree


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
    # print('timezone.now : ', timezone.now())
    # print('alert_end : ', weathers.alert_end)
    # print(timezone.localtime(timezone.now()))

    if weathers.alert_end and weathers.alert_end > timezone.now():
        alert = True
    else:
        alert = False

    unites = request.user.weather.unites

    if unites == '2':
        u1, u2 = '°F', 'miles/hour'
    elif unites == '3':
        u1, u2 = '°K', 'm/s'
    else:
        u1, u2 = '°C', 'm/s'
        weathers.wwind_speed0kmh = float(weathers.wwind_speed0) * 3.6
        weathers.wwind_speed0kmh = "{:.2f}".format(weathers.wwind_speed0kmh)
        weathers.wwind_gust0kmh = float(weathers.wwind_gust0) * 3.6
        weathers.wwind_gust0kmh = "{:.2f}".format(weathers.wwind_gust0kmh)
        weathers.wwind_speed1kmh = float(weathers.wwind_speed1) * 3.6
        weathers.wwind_speed1kmh = "{:.2f}".format(weathers.wwind_speed1kmh)
        weathers.wwind_gust1kmh = float(weathers.wwind_gust1) * 3.6
        weathers.wwind_gust1kmh = "{:.2f}".format(weathers.wwind_gust1kmh)
        weathers.wwind_speed2kmh = float(weathers.wwind_speed2) * 3.6
        weathers.wwind_speed2kmh = "{:.2f}".format(weathers.wwind_speed2kmh)
        weathers.wwind_gust2kmh = float(weathers.wwind_gust2) * 3.6
        weathers.wwind_gust2kmh = "{:.2f}".format(weathers.wwind_gust2kmh)
        weathers.wwind_speed3kmh = float(weathers.wwind_speed3) * 3.6
        weathers.wwind_speed3kmh = "{:.2f}".format(weathers.wwind_speed3kmh)
        weathers.wwind_gust3kmh = float(weathers.wwind_gust3) * 3.6
        weathers.wwind_gust3kmh = "{:.2f}".format(weathers.wwind_gust3kmh)
        weathers.wwind_speed4kmh = float(weathers.wwind_speed4) * 3.6
        weathers.wwind_speed4kmh = "{:.2f}".format(weathers.wwind_speed4kmh)
        weathers.wwind_gust4kmh = float(weathers.wwind_gust4) * 3.6
        weathers.wwind_gust4kmh = "{:.2f}".format(weathers.wwind_gust4kmh)

    context = {'title': _('Weather'), 'weathers': weathers, 'sync': sync, 'u1': u1, 'u2': u2, 'alert': alert,
               'localti': "Europe/Paris"}  # TODO modify with user timezone
    return render(request, 'users/weather.html', context)


@login_required
def pubprofile(request, pk):
    ownerobj = get_object_or_404(User, pk=pk)
    if ownerobj == request.user or ownerobj.profile.public_profile is True:
        trees = Tree.objects.filter(ownerfk=ownerobj)

        photos = Photo.objects.filter(treefk__ownerfk=ownerobj).order_by('shot_date')
        paginator = Paginator(photos, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'owner': ownerobj, 'trees': trees, 'page_obj': page_obj}
        print(context)
        return render(request, 'users/public_profile.html', context)
    else:
        mes = _("Are you trying to list private pictures?")
        messages.warning(request, mes)
        return redirect('core-tdb')
