from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_profile = models.BooleanField(default=False, verbose_name=_('Public profile'))
    lat = models.DecimalField(_('Latitude'), default='48.856643', max_digits=10, decimal_places=6)
    long = models.DecimalField(_('Longitude'), default='2.352566', max_digits=10, decimal_places=6)
    weather = models.BooleanField(default=False, verbose_name=_('Weather alert'))
    max_temp = models.IntegerField(default=30, verbose_name=_('Max temperature (°C)'))
    min_temp = models.IntegerField(default=2, verbose_name=_('Min temperature (°C)'))
    max_wind = models.IntegerField(default=50, verbose_name=_('Gust speed (km/h)'))
    last_year = datetime.today()-timedelta(days=365)
    don_date = models.DateField(default=last_year)
    valid_user = models.BooleanField(default=False, verbose_name=_('Valid user'))

    def __str__(self):
        return f'{ self.user.username } Profile'
