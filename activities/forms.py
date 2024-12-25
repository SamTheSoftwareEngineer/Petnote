from django import forms
from .models import Activity

ACTIVITY_CHOICES = [
        ("Walk", "Walk"),
        ("Play", "Play"),
        ("Feed", "Feed"),
        ("Vet", "Vet"),
        ("Groom", "Groom"),
        ("Training", "Training"),
        ("Medicine", "Medicine"),
        ("Other", "Other"),
    ]
    
class ActivityForm(forms.ModelForm):
    activity_type = forms.ChoiceField(choices=ACTIVITY_CHOICES, required=False)
    class Meta:
        model = Activity
        fields = ['name', 'description', 'pet', 'activity_type', 'is_completed', 'notes'] 