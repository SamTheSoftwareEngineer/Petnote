from django import forms 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm

User = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model= User
        fields = (
            "email",
            "username"
        )
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "email",
            "username"
        )

class ProfileUpdateForm(forms.ModelForm):
    profile_image = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ["username", "bio", "profile_image"]
    
class CustomSignupForm(SignupForm):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    email2 = forms.EmailField(label="Confirm Email", widget=forms.EmailInput(attrs={'placeholder': 'Confirm your email'}))

    def clean_email2(self):
        email1 = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")

        if email1 != email2:
            raise forms.ValidationError("The two email addresses must match.")
        return email2
