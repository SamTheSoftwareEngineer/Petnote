from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm, ProfileUpdateForm, CustomUserCreationForm
from django.contrib import messages
from pets.models import Pet
from django.contrib.auth import login, authenticate, logout

def index(request):
    # Check if the user is authenticated and redirect to the profilepage 
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        # If the user is not authenticated, render the index template
        return render(request, 'core/index.html')
    

def signup(request):
    """Handles user registration and logs the user in upon successful signup."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()  # Save user to database
                messages.success(request, 'Account created successfully!')

                # Authenticate the user before logging in
                user = authenticate(request, username=user.username, password=request.POST['password1'])

                if user:
                    login(request, user)  # Log user in
                    return redirect('profile')  # Redirect to a logged-in page

            except Exception as e:
                messages.error(request, f"Error creating user: {e}")
                return redirect('signup')

    else:
        form = CustomUserCreationForm()
    
    return render(request, 'account/signup.html', {'form': form})


def verification_sent(request):
    return render(request, 'core/verification_sent.html')

def verification_success(request):
    return render(request, 'core/verification_success.html')


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

def logout_view(request):
    # Log the user out
    logout(request)

    return render(request, 'core/thanks.html')


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
