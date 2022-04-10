from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from django.utils.translation import gettext as _


class Species(models.Model):
    sname = models.CharField(max_length=100)

    def __str__(self):
        return self.sname

class Origin(models.Model):
    oname = models.CharField(max_length=100)

    def __str__(self):
        return self.oname

class Tree(models.Model):
    tname = models.CharField(max_length=100, verbose_name=_('Name'))
    originfk = models.ForeignKey(Origin, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Origin'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    speciesfk = models.ForeignKey(Species, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Species'))
    bdate = models.DateField(null=True, blank=True, verbose_name=_('Planting date'))
    adate = models.DateField(null=True, blank=True, default=timezone.now, verbose_name=_('Acquisition date'))
    ownerfk = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Owner'))
    treePic = models.ImageField(default='default.png', upload_to='tree_pics', verbose_name=_('Main picture'))

    def __str__(self):
        return self.tname

    def get_absolute_url(self):
        return reverse('tree-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.id and not self.treePic:
            return
        super(Tree, self).save(*args, **kwargs)

        img = Image.open(self.treePic)
        (width, height) = img.size

        # resize @ 300px small size
        if 300 / width < 300 / height:
            factor = 300 / height
        else:
            factor = 300 / width

        size = (int(width * factor), int(height * factor))
        img = img.resize(size, Image.ANTIALIAS)
        (width, height) = img.size

        # crop @ 300 x 300 px
        x1 = int((width - 300) / 2)
        y1 = int((height - 300) / 2)
        x2 = int((width + 300) / 2)
        y2 = int((height + 300) / 2)
        img = img.crop((x1, y1, x2, y2))

        img.save(self.treePic.path)

class Tasklist(models.Model):
    tlname = models.CharField(max_length=100, verbose_name=_('Name'))

    def __str__(self):
        return self.tlname

class Task(models.Model):
    tasklistfk = models.ForeignKey(Tasklist, default=1, on_delete=models.SET_DEFAULT, verbose_name=_('Type'))
    treefk = models.ForeignKey(Tree, on_delete=models.CASCADE, verbose_name=_('Tree'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    plan_date = models.DateField(null=True, blank=True, verbose_name=_('Planned date'))
    real_date = models.DateField(null=True, blank=True, verbose_name=_('Realisation date'))

    def get_absolute_url(self):
        return reverse('tree-detail', kwargs={'pk': self.treefk.id})