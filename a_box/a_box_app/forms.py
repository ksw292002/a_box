from __future__ import unicode_literals

from django import forms

# User Sign Up, Sign In function 구현
from django.contrib.auth.models import User

from .models import StoredFiles


class FileUpForm(forms.ModelForm):
    class Meta:
        model = StoredFiles
        fields = ('content', )

# User Sign Up function 구현
class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = ('username', 'email', 'password', )

# Login function 구현
class SigninForm(forms.ModelForm) :
    class Meta:
        model = User
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = ('username', 'password',)