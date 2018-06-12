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
            'username': forms.TextInput(attrs={'class': 'form-control', 'id': 'exampleInputName2', 'placeholder': '아이디를 입력하세요'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'exampleInputEmail1', 'placeholder': '이메일을 입력하세요'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'exampleInputPassword1', 'placeholder': '암호'}),
        }
        fields = ('username', 'email', 'password', )

# Login function 구현
class SigninForm(forms.ModelForm) :
    class Meta:
        model = User
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'id': 'exampleInputName2', 'placeholder': '아이디를 입력하세요'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'exampleInputPassword1', 'placeholder': '암호'}),
        }
        fields = ('username', 'password',)
