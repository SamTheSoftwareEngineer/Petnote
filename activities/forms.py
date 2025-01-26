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
    class Meta:
        model = Activity
        fields = [ 'activity_type','description', 'pet', 'activity_name', 'is_completed', 'notes', 'date_completed'] 
        widgets = {
            'date_completed': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # For date and time input
        }
        