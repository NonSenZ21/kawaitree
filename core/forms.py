from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Task, Photo, Species, Tree


class TaskCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        self.fields['treefk'].empty_label = None

    class Meta:
        model = Task
        fields = ['tasklistfk', 'treefk', 'description', 'plan_date', 'real_date', 'url']


class TaskUpdateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(TaskUpdateForm, self).__init__(*args, **kwargs)
        self.fields['treefk'].empty_label = None

    class Meta:
        model = Task
        fields = ['tasklistfk', 'treefk', 'description', 'plan_date', 'real_date', 'url']


class PhotoCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(PhotoCreateForm, self).__init__(*args, **kwargs)
        self.fields['treefk'].empty_label = None

    class Meta:
        model = Photo
        fields = ['treefk', 'taskfk', 'description', 'shot_date', 'before_pic', 'after_pic', 'picture', 'thumb']


class PhotoListallFormTree(ModelForm):
    class Meta:
        model = Tree
        fields = ['ownerfk', 'speciesfk']

    def __init__(self, *args, **kwargs):
        super(PhotoListallFormTree, self).__init__(*args, **kwargs)
        self.fields['ownerfk'].required = False
        self.fields['ownerfk'].queryset = User.objects.filter(profile__public_profile=True).order_by('username')
