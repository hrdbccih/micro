from .models import Culturatemp
from django import forms


class Culturatempform(forms.ModelForm):

    class Meta:
        model = Culturatemp
        fields = '__all__'

