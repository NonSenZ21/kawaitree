from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from datetime import datetime
from django.utils.translation import gettext_lazy as _
import os
from .imgtransform import image_autorotate


class Species(models.Model):
    cat = models.CharField(max_length=3, default='A')
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('cat', 'name')

    def __str__(self):
        specstr = str(self.cat) + ' - ' + str(self.name)
        return specstr


class Origin(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tree(models.Model):
    tname = models.CharField(max_length=100, verbose_name=_('Name'))
    originfk = models.ForeignKey(Origin, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Origin'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    speciesfk = models.ForeignKey(Species, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Species'))
    bdate = models.DateField(null=True, blank=True, verbose_name=_('Planting date'))
    adate = models.DateField(null=True, blank=True, default=timezone.now, verbose_name=_('Acquisition date'))
    ownerfk = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Owner'))
    treePic = models.ImageField(default='default.png', upload_to='tree_pics', verbose_name=_('Main picture'))
    url = models.URLField(blank=True, null=True, verbose_name=_('URL (YouTube video...)'))

    def __str__(self):
        return self.tname

    def get_absolute_url(self):
        return reverse('tree-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.id and not self.treePic:
            return
        super(Tree, self).save(*args, **kwargs)

        # img = Image.open(self.treePic)
        img = image_autorotate(self.treePic)
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
    name = models.CharField(max_length=100, verbose_name=_('Name'))

    def __str__(self):
        return self.name


class Task(models.Model):
    tasklistfk = models.ForeignKey(Tasklist, default=1, on_delete=models.SET_DEFAULT, verbose_name=_('Type'))
    treefk = models.ForeignKey(Tree, on_delete=models.CASCADE, verbose_name=_('Tree'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    plan_date = models.DateField(null=True, blank=True, verbose_name=_('Planned date'))
    real_date = models.DateField(null=True, blank=True, verbose_name=_('Realisation date'))
    url = models.URLField(blank=True, null=True, verbose_name=_('URL (YouTube video...)'))

    def get_absolute_url(self):
        return reverse('tree-detail', kwargs={'pk': self.treefk.id})

    def __str__(self):
        if self.real_date:
            real_date = self.real_date.strftime('%d/%m/%Y')
            task_string = self.treefk.__str__() + " - " + self.tasklistfk.__str__() + " - " + str(real_date)
        else:
            plan_date = self.plan_date.strftime('%d/%m/%Y')
            task_string = self.treefk.__str__() + " - " + self.tasklistfk.__str__() + " - " + str(plan_date)
        return task_string


class Photo(models.Model):
    treefk = models.ForeignKey(Tree, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('Tree'))
    taskfk = models.ForeignKey(Task, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('Task'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    shot_date = models.DateField(null=True, blank=True, default=timezone.now, verbose_name=_('Shot date'))
    before_pic = models.BooleanField(default=False, verbose_name=_('Shot before task'))
    after_pic = models.BooleanField(default=False, verbose_name=_('Shot after task'))
    picture = models.ImageField(upload_to='trees-tasks_pics', verbose_name=_('Picture'))
    thumb = models.ImageField(default='thumbs/default-thumb.png', upload_to='thumbs', verbose_name=_('Thumbnail'))

    def get_absolute_url(self):
        return reverse('photo-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):

        if not self.id and not self.picture:
            return

        self.thumb.name = os.path.join(os.path.split(self.thumb.name)[0], os.path.split(self.picture.path)[-1])

        super().save(*args, **kwargs)

        # img = Image.open(self.picture)
        img = image_autorotate(self.picture)
        (width, height) = img.size

        # resize @ 1200 x 800 max size
        if width > 1200 or height > 800:
            ratio = width / height
            if ratio > 1.5:
                size = (1200, int(1200 / ratio))
            else:
                size = (int(800 * ratio), 800)

            img = img.resize(size, Image.ANTIALIAS)
            (width, height) = img.size

        img.save(self.picture.path, 'JPEG', quality=85)

        # resize thumbnail @ 150 px height max size
        # thumb = Image.open(self.thumb)
        thumb = img
        if height > 150:
            ratio = width / height
            size = (int(150 * ratio), 150)
            thumb = thumb.resize(size, Image.ANTIALIAS)

        thumb.save(self.thumb.path, 'JPEG')
        thumb.close()
        img.close()


class Linkcat(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))

    def __str__(self):
        return self.name


class Link(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    order = models.IntegerField(default=10, verbose_name=_('order'))
    linkcatfk = models.ForeignKey(Linkcat, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Category'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    image = models.ImageField(upload_to='links_pics', verbose_name=_('Logo'))
    url = models.URLField(blank=True, null=True, verbose_name=_('URL'))

    def __str__(self):
        return self.name
