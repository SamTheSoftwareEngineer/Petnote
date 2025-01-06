from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, UpdateUsernameForm, UserCreationForm
from pets.models import Pet

def index(request):
    # Check if the user is authenticated and redirect to the pet page 
    if request.user.is_authenticated:
        return redirect('pet_list')
    else:
        # If the user is not authenticated, render the index template
        return render(request, 'core/index.html')

@login_required
def profile_view(request):
    profile = request.user.userprofile
    pets_count = Pet.objects.filter(user=request.user).count()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    context = {
        'form': form,
        'pets': pets_count,
        'profile': profile,
        'pets_count': pets_count
    }
    return render(request, 'core/profile.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('pet_list')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

def thanks_view(request):
    return render(request, 'core/thanks.html')

@login_required
def update_username(request):
    if request.method == 'POST':
        form = UpdateUsernameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()  # Save the updated username
            return redirect('profile')  # Redirect to the user's profile page (adjust this URL name if necessary)
    else:
        form = UpdateUsernameForm(instance=request.user)

    return render(request, 'core/update_username.html', {'form': form})