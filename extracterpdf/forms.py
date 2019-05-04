from .models import Destinos
from django import forms
from django.forms import ClearableFileInput

class Destinosform(forms.ModelForm):

    class Meta:
        model = Destinos
        fields = '__all__'
        widgets = {
            'pdffile': ClearableFileInput(attrs={'multiple': True}),
        }
