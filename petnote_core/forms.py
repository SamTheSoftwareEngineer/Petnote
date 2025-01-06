from django import forms 
from .models import UserProfile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us about yourself!'}),
        }

class UpdateUsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise ValidationError("This username is already taken.")
        return username


