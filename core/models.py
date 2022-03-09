from django.db import models
from django.contrib.auth.models import User

class Species(models.Model):
    sname = models.CharField(max_length=100)

    def __str__(self):
        return self.sname

class Tree(models.Model):
    tname = models.CharField(max_length=100)
    shop = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    speciesfk = models.ForeignKey(Species, on_delete=models.CASCADE)
    bdate = models.DateField(null=True, blank=True)
    adate = models.DateField(null=True, blank=True)
    ownerfk = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.tname




