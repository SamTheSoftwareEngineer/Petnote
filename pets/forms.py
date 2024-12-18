from django import forms
from .models import Pet

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['photo','name', 'species', 'age', 'weight', 'breed', 'birth_date']