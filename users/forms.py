from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_id = 'uc_form'
    #     self.helper.form_method = 'post'
    #     self.helper.form_action = 'profile'


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['public_profile', 'lat', 'long', 'weather', 'unites', 'max_temp', 'min_temp',
                  'max_wind', 'fb', 'yt', 'insta', 'web', 'valid_user', 'expert']
