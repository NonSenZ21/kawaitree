from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_profile = models.BooleanField(default=False, verbose_name=_('Public profile'))
    lat = models.DecimalField(_('Latitude'), default='48.856643', max_digits=10, decimal_places=6)
    long = models.DecimalField(_('Longitude'), default='2.352566', max_digits=10, decimal_places=6)
    weather = models.BooleanField(default=False, verbose_name=_('Weather alerts'))
    choix = (('1', _('Metric (°C, m/s)')), ('2', _('Imperial (°F, miles/hour)')), ('3', _('Standard (°K, m/s)')))
    unites = models.CharField(max_length=1, default='1', choices=choix, verbose_name=_('Units'))
    max_temp = models.IntegerField(default=30, verbose_name=_('Max temperature'))
    min_temp = models.IntegerField(default=2, verbose_name=_('Min temperature'))
    max_wind = models.IntegerField(default=15, verbose_name=_('Gust speed'))
    fb = models.URLField(verbose_name='Facebook', blank=True, null=True)
    yt = models.URLField(verbose_name='Youtube', blank=True, null=True)
    insta = models.URLField(verbose_name='Instagram', blank=True, null=True)
    web = models.URLField(verbose_name=_('Website'), blank=True, null=True)
    don_date = models.DateField(null=True, blank=True, default=date(2021, 1, 1), verbose_name=_('Last donation date'))
    valid_user = models.BooleanField(default=False, verbose_name=_('Valid user'))
    expert = models.BooleanField(default=False, verbose_name=_('Expert (disable helpers)'))

    def __str__(self):
        return f'{self.user.username} Profile'


class Weather(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unites = models.CharField(max_length=1, default='1', verbose_name=_('Units'))
    alert_sender = models.CharField(null=True, blank=True, max_length=100, verbose_name=_('Alert sender'))
    alert_event = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Event'))
    alert_start = models.DateTimeField(null=True, blank=True, verbose_name=_('Start'))
    alert_end = models.DateTimeField(null=True, blank=True, verbose_name=_('End'))
    alert_description = models.TextField(null=True, blank=True, verbose_name=_('Alert description'))

    def __str__(self):
        return f'{self.user.username} Weather'

class Weatherday(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wnday = models.IntegerField(default=0, verbose_name=_('Day number'))
    wdate = models.DateField(default=date(2021, 1, 1), verbose_name=_('Date'))
    wid = models.IntegerField(default=0, verbose_name=_('Weather code'))
    wmain = models.CharField(null=True, blank=True, max_length=100, verbose_name=_('Weather main'))
    wdescription = models.CharField(null=True, blank=True, max_length=150, verbose_name=_('Weather description'))
    wpressure = models.IntegerField(default=0, verbose_name=_('Pressure'))
    wtemp_min = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                     verbose_name=_('Min temperature'))
    wtemp_max = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                     verbose_name=_('Max temperature'))
    wwind_speed = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                       verbose_name=_('Wind speed'))
    wwind_gust = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                      verbose_name=_('Gusts speed'))
    whumidity = models.IntegerField(default=0, verbose_name=_('Humidity'))
    wrain = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                 verbose_name=_('Rain'))
    wicon = models.CharField(null=True, blank=True, max_length=10, verbose_name=_('Weather icon'))
