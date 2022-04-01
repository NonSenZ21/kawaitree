from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Tree

class TreeUpdateForm(forms.ModelForm):
    class Meta:
        model = Tree
        fields = ['tname', 'shop', 'description', 'speciesfk', 'bdate', 'adate', 'treePic']
