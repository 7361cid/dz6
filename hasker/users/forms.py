from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "profile_avatar")


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        exclude = ('username', 'password', 'first_name', 'is_superuser', 'date_joined', 'user_permissions',
                   'last_name', 'is_staff', 'is_active', 'last_login', 'groups')
