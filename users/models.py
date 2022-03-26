from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_profile = models.BooleanField(default=False)
    lat = models.DecimalField(_('Latitude'), default='48.856643', max_digits=10, decimal_places=6)
    long = models.DecimalField(_('Longitude'), default='2.352566', max_digits=10, decimal_places=6)

    def __str__(self):
        return f'{ self.user.username } Profile'
