from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# This form is not currently used, but I included in case you need to design a custom UserRegistrationForm where
# you can ask the user to enter email and password instead of password and username to register your site
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']