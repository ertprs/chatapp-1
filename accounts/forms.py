from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Picture, Preferences

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ['pic',]


class LoginForm(forms.models.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.fields.TextInput(attrs={
                'placeholder': "Username",
                'class': '',
                'id': '',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': "Password",
                'class': '',
            }),
        }
        labels = {
            'username': '',
            'password': '',
        }

class RegisterForm(UserCreationForm, forms.models.ModelForm):
    password1 = forms.CharField(label=(''),
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Password',
                                    'class': 'mt-5',
                                }))
    password2 = forms.CharField(label='',
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Password confirmation',
                                    'class': 'mt-5',
                                }),
                                help_text="Enter the same password as above, for verification"
                                )
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.fields.TextInput(attrs={
                'placeholder': "Username",
                'class': 'mt-4',
                'id': 'signup-username',
            }),

        }

        labels = {
            'username': ''
        }


class PreferencesForm(forms.models.ModelForm):
    username = forms.CharField(max_length=20, required=False, empty_value='')
    email = forms.EmailField(required=False, empty_value='')
    bio = forms.CharField(max_length=50, required=False, empty_value='')
    class Meta:
        model = Preferences
        fields = ['username', 'email', 'bio']


    # username = forms.CharField(label='', max_length=20, required=False, widget=forms.TextInput(attrs={
    #     'placeholder': 'username'
    #
    # }))
    # email = forms.EmailField(required=False, label='', widget=forms.EmailInput(attrs={
    #     'placeholder': 'email',
    #     'class': 'mt-4'
    # }))
    # bio = forms.CharField(max_length=50, required=False, label='', widget=forms.TextInput(attrs={
    #     'placeholder': 'bio',
    #     'class': 'mt-4'
    # }))


class PasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'placeholder': 'current password',
        'disabled': True

    }))
    new_password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'placeholder': 'new password',
        'class': 'mt-4',
        'disabled': True
    }))
    new_password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'placeholder': 'confirm password',
        'class': 'mt-4',
        'disabled': True
    }))


