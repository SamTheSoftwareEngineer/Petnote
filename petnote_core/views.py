from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib import messages
from pets.models import Pet
from .forms import ProfileUpdateForm



def index(request):
    # Check if the user is authenticated and redirect to the pet page 
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        # If the user is not authenticated, render the index template
        return render(request, 'core/index.html')


@login_required
def profile_view(request):
    user = request.user
    pets_count = Pet.objects.filter(user=user).count()  # Count user’s pets

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile")  # Redirect after updating
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, "core/profile.html", {
        "user": user,
        "pets_count": pets_count,
        "form": form
    })


def signup(request):
    """Handles user registration and sends a verification email."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the user to the database
            try:
                form.save()
                # Show success message to user
                messages.success(request, 'Account created successfully!')
                return redirect('login')
            except Exception as e:
                messages.error(request, f"Error creating user: {e}")
                return redirect('signup')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})

def thanks_view(request):
    return render(request, 'core/thanks.html')

@login_required
def update_username(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()  # Save the updated username
            return redirect('profile')  # Redirect to the user's profile page 
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'core/update_username.html', {'form': form})

