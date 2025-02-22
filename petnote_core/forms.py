from django import forms 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

# Form to create a new user
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model= User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2"
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring focus:ring-blue-300'
            })

# Form to change email
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "email",
        )

# Form to update profile
class ProfileUpdateForm(forms.ModelForm):
    profile_image = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ["first_name", "bio", "profile_image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring focus:ring-blue-300'
            })


    
