# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _


@login_required
def profile(request):
    if request.method == 'POST':
        uc_form = UserUpdateForm(request.POST, instance=request.user)
        pc_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
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