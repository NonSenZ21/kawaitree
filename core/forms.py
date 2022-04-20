from django.forms import ModelForm
from .models import Task, Photo


class TaskCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(TaskCreateForm, self).__init__(*args, **kwargs)  # populates the post
        self.fields['treefk'].empty_label = None

    class Meta:
        model = Task
        fields = ['tasklistfk', 'treefk', 'description', 'plan_date', 'real_date', 'url']


class TaskUpdateForm(ModelForm):

    class Meta:
        model = Task
        fields = ['tasklistfk', 'treefk', 'description', 'plan_date', 'real_date', 'url']


class PhotoCreateForm(ModelForm):

    class Meta:
        model = Photo
        fields = ['treefk', 'taskfk', 'description', 'shot_date', 'before_pic', 'after_pic', 'picture', 'thumb']
