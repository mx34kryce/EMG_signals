from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    auth_code = forms.IntegerField(label="인증 코드", required=True)  # Add the auth_code field here

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email", "auth_code")

