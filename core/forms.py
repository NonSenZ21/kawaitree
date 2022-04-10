from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Task,Tree


class TaskCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(TaskCreateForm, self).__init__(*args, **kwargs)  # populates the post
        self.fields['treefk'].empty_label = None

    class Meta:
        model = Task
        fields = ['tasklistfk', 'treefk', 'description', 'plan_date', 'real_date']

class TaskUpdateForm(ModelForm):

    class Meta:
        model = Task
        fields = ['tasklistfk', 'treefk', 'description', 'plan_date', 'real_date']
