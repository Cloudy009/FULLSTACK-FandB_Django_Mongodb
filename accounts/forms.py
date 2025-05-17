# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',  # Thêm class Bootstrap
        'placeholder': 'Enter your email'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your username'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm your password'
    }))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser


# class AdditionalInfoForm(forms.ModelForm):
#     phone_number = forms.CharField(
#         label=_("Phone Number"),
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
#     )
#     address = forms.CharField(
#         label=_("Address"),
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
#     )

#     class Meta:
#         model = UserProfile  # Giả sử bạn có một model UserProfile lưu thông tin bổ sung
#         fields = ('phone_number', 'address')
