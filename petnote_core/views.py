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
