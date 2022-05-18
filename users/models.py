from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
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
    last_year = datetime.today() - timedelta(days=365)
    don_date = models.DateField(null=True, blank=True, default=last_year, verbose_name=_('Last donation date'))
    valid_user = models.BooleanField(default=False, verbose_name=_('Valid user'))
    expert = models.BooleanField(default=False, verbose_name=_('Expert (disable helpers)'))

    def __str__(self):
        return f'{self.user.username} Profile'


class Weather(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wnday0 = models.IntegerField(default=0, verbose_name=_('Day number'))
    wdate0 = models.DateField(default=timezone.now, verbose_name=_('Date'))
    wid0 = models.IntegerField(default=0, verbose_name=_('Weather code'))
    wmain0 = models.CharField(null=True, blank=True, max_length=100, verbose_name=_('Weather main'))
    wdescription0 = models.CharField(null=True, blank=True, max_length=150, verbose_name=_('Weather description'))
    wpressure0 = models.IntegerField(default=0, verbose_name=_('Pressure'))
    wtemp_min0 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                     verbose_name=_('Min temperature'))
    wtemp_max0 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                     verbose_name=_('Max temperature'))
    wwind_speed0 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                       verbose_name=_('Wind speed'))
    wwind_gust0 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                      verbose_name=_('Gusts speed'))
    whumidity0 = models.IntegerField(default=0, verbose_name=_('Humidity'))
    wrain0 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                 verbose_name=_('Rain'))
    wicon0 = models.CharField(null=True, blank=True, max_length=10, verbose_name=_('Weather icon'))

    wnday1 = models.IntegerField(default=0, verbose_name=_('Day number'))
    wdate1 = models.DateField(default=timezone.now, verbose_name=_('Date'))
    wid1 = models.IntegerField(default=0, verbose_name=_('Weather code'))
    wmain1 = models.CharField(null=True, blank=True, max_length=100, verbose_name=_('Weather main'))
    wdescription1 = models.CharField(null=True, blank=True, max_length=150, verbose_name=_('Weather description'))
    wpressure1 = models.IntegerField(default=0, verbose_name=_('Pressure'))
    wtemp_min1 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                     verbose_name=_('Min temperature'))
    wtemp_max1 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                     verbose_name=_('Max temperature'))
    wwind_speed1 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                       verbose_name=_('Wind speed'))
    wwind_gust1 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                      verbose_name=_('Gusts speed'))
    whumidity1 = models.IntegerField(default=0, verbose_name=_('Humidity'))
    wrain1 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                 verbose_name=_('Rain'))
    wicon1 = models.CharField(null=True, blank=True, max_length=10, verbose_name=_('Weather icon'))

    wnday2 = models.IntegerField(default=0, verbose_name=_('Day number'))
    wdate2 = models.DateField(default=timezone.now, verbose_name=_('Date'))
    wid2 = models.IntegerField(default=0, verbose_name=_('Weather code'))
    wmain2 = models.CharField(null=True, blank=True, max_length=100, verbose_name=_('Weather main'))
    wdescription2 = models.CharField(null=True, blank=True, max_length=150, verbose_name=_('Weather description'))
    wpressure2 = models.IntegerField(default=0, verbose_name=_('Pressure'))
    wtemp_min2 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                     verbose_name=_('Min temperature'))
    wtemp_max2 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                     verbose_name=_('Max temperature'))
    wwind_speed2 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                       verbose_name=_('Wind speed'))
    wwind_gust2 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                      verbose_name=_('Gusts speed'))
    whumidity2 = models.IntegerField(default=0, verbose_name=_('Humidity'))
    wrain2 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                 verbose_name=_('Rain'))
    wicon2 = models.CharField(null=True, blank=True, max_length=10, verbose_name=_('Weather icon'))

    wnday3 = models.IntegerField(default=0, verbose_name=_('Day number'))
    wdate3 = models.DateField(default=timezone.now, verbose_name=_('Date'))
    wid3 = models.IntegerField(default=0, verbose_name=_('Weather code'))
    wmain3 = models.CharField(null=True, blank=True, max_length=100, verbose_name=_('Weather main'))
    wdescription3 = models.CharField(null=True, blank=True, max_length=150, verbose_name=_('Weather description'))
    wpressure3 = models.IntegerField(default=0, verbose_name=_('Pressure'))
    wtemp_min3 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                     verbose_name=_('Min temperature'))
    wtemp_max3 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                     verbose_name=_('Max temperature'))
    wwind_speed3 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                       verbose_name=_('Wind speed'))
    wwind_gust3 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                      verbose_name=_('Gusts speed'))
    whumidity3 = models.IntegerField(default=0, verbose_name=_('Humidity'))
    wrain3 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                 verbose_name=_('Rain'))
    wicon3 = models.CharField(null=True, blank=True, max_length=10, verbose_name=_('Weather icon'))

    wnday4 = models.IntegerField(default=0, verbose_name=_('Day number'))
    wdate4 = models.DateField(default=timezone.now, verbose_name=_('Date'))
    wid4 = models.IntegerField(default=0, verbose_name=_('Weather code'))
    wmain4 = models.CharField(null=True, blank=True, max_length=100, verbose_name=_('Weather main'))
    wdescription4 = models.CharField(null=True, blank=True, max_length=150, verbose_name=_('Weather description'))
    wpressure4 = models.IntegerField(default=0, verbose_name=_('Pressure'))
    wtemp_min4 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                     verbose_name=_('Min temperature'))
    wtemp_max4 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                     verbose_name=_('Max temperature'))
    wwind_speed4 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                       verbose_name=_('Wind speed'))
    wwind_gust4 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                      verbose_name=_('Gusts speed'))
    whumidity4 = models.IntegerField(default=0, verbose_name=_('Humidity'))
    wrain4 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5,
                                 verbose_name=_('Rain'))
    wicon4 = models.CharField(null=True, blank=True, max_length=10, verbose_name=_('Weather icon'))
    alert_sender = models.CharField(null=True, blank=True, max_length=100, verbose_name=_('Alert sender'))
    alert_event = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Event'))
    alert_start = models.DateTimeField(null=True, blank=True, verbose_name=_('Start'))
    alert_end = models.DateTimeField(null=True, blank=True, verbose_name=_('End'))
    alert_description = models.TextField(null=True, blank=True, verbose_name=_('Alert description'))

    def __str__(self):
        return f'{self.user.username} Weather'
