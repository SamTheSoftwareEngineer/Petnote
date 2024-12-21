from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from pets.models import Pet

def index(request):
    return render(request, 'core/index.html')
@login_required
def profile_view(request):
    profile = request.user.userprofile
    pets = Pet.objects.filter(user=request.user).count()

    # If the request method is post, meaning they are updating their profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            print("Form is valid, saving profile...")
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
        print(form.errors)

    return render(request, 'core/profile.html', {'form': form, 'pets': pets})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after sign-up
            return redirect('pet_list')  # Redirect to the pet list page
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})
