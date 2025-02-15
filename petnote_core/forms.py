from django import forms 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username"
        )
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username"
        )

class UpdateUsernameForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if get_user_model().objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise ValidationError("This username is already taken.")
        return username

    

