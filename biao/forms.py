from django.contrib.auth.models import User
from django import forms
from .models import Cultura


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'autocomplete': 'off'}),
            'email': forms.TextInput(attrs={'autocomplete': 'off'}),
            'password': forms.TextInput(attrs={'autocomplete': 'off'}),
        }


class Culturaform(forms.ModelForm):

    class Meta:
        model = Cultura
        fields = '__all__'
