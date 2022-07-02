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
from .models import Weather, Weatherday
from core.models import Photo, Tree


@login_required
def profile(request):
    if request.method == 'POST':
        print("post")
        uc_form = UserUpdateForm(request.POST, instance=request.user)
        pc_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if uc_form.is_valid() and pc_form.is_valid():
            print("valid")
            uc_form.save()
            pc_form.save()
            mes_suc = _('Your account has been updated!')
            messages.success(request, mes_suc)
            return redirect('profile')
        else:
            print("request.POST", request.POST)
            mes_warn = _('Something went wrong!')
            messages.warning(request, mes_warn)
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


def complete(request, wd):
    if wd.wtemp_min <= request.user.profile.min_temp:
        wd.wtemp_min_warn = True
    else:
        wd.wtemp_min_warn = False
    if wd.wtemp_max >= request.user.profile.max_temp:
        wd.wtemp_max_warn = True
    else:
        wd.wtemp_max_warn = False
    if wd.wwind_gust >= request.user.profile.max_wind:
        wd.wwind_gust_warn = True
    else:
        wd.wwind_gust_warn = False
    return wd


@login_required
def weather(request):
    if not request.user.profile.weather:
        mes = _('Weather is not enabled in your profile.')
        messages.warning(request, mes)
        return redirect('profile')

    weathers = Weather.objects.get(user=request.user)
    weatherdays = Weatherday.objects.filter(user=request.user)
    # print("weatherdays: ", weatherdays)
    if not weatherdays:
        mes = _('No information for now. Make sure you checked the "Weather alerts" checkbox in your profile and you '
                'will get your weather here tomorrow.')
        messages.warning(request, mes)
        return redirect('profile')
    elif weatherdays[0].wdate != date.today():
        mes = _('No information for now. Make sure you checked the "Weather alerts" checkbox in your profile and you '
                'will get your weather here tomorrow.')
        messages.warning(request, mes)
        return redirect('profile')

    # print('timezone.now : ', timezone.now())
    # print('alert_end : ', weathers.alert_end)
    # print(timezone.localtime(timezone.now()))

    if weathers.alert_end and weathers.alert_end > timezone.now():
        alert = True
    else:
        alert = False

    unites = request.user.weather.unites
    wdtab = []
    if unites == '2':
        u1, u2 = '°F', 'miles/hour'
        for weatherday in weatherdays:
            wdalert = complete(request, weatherday)
            wdtab.append(wdalert)

    elif unites == '3':
        u1, u2 = '°K', 'm/s'
        for weatherday in weatherdays:
            wdalert = complete(request, weatherday)
            wdtab.append(wdalert)

    else:
        u1, u2 = '°C', 'm/s'
        for weatherday in weatherdays:
            wdalert = weatherday
            wdalert.wwind_speedkmh = "{:.2f}".format(float(weatherday.wwind_speed) * 3.6)
            wdalert.wwind_gustkmh = "{:.2f}".format(float(weatherday.wwind_gust) * 3.6)
            wdalert = complete(request, weatherday)
            wdtab.append(wdalert)

    context = {'title': _('Weather'), 'weathers': weathers, 'weatherdays': wdtab,
               'u1': u1, 'u2': u2,
               'alert': alert, 'localti': "Europe/Paris"}   # TODO modify with user timezone

    return render(request, 'users/weather.html', context)


@login_required
def pubprofile(request, pk):
    ownerobj = get_object_or_404(User, pk=pk)
    if ownerobj == request.user or ownerobj.profile.public_profile is True:
        trees = Tree.objects.filter(ownerfk=ownerobj)
        photos = Photo.objects.filter(treefk__ownerfk=ownerobj).order_by('-shot_date')
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
