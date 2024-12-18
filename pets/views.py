from django.shortcuts import render, redirect, get_object_or_404
from .models import Pet
from .forms import PetForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def pet_list(request):
    pets = Pet.objects.all() # get all pets from the database
    return render(request, 'pets/pet_list.html', {'pets': pets})

def add_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        # Check to see if the form is valid
        if form.is_valid():
            pet = form.save(commit=False)
            # Associate the pet with the logged in user 
            pet.user = request.user
            pet.save()
            # Redirect to the pet list 
            return redirect('pet_list')
    else:
        form = PetForm()

    return render(request, 'pets/add_pet.html', {'form': form})

def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'pets/pet_detail.html', {'pet': pet})

def edit_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('pet_detail', pet_id=pet.id)
    else:
        form = PetForm(instance=pet)
    return render(request, 'pets/edit_pet.html', {'form': form, 'pet': pet})

def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method =="POST":
        pet.delete()
        return redirect('pet_list')
    return render(request, 'pets/delete_pet.html', {'pet': pet})

@login_required
def pet_list_auth(request):
    pets = Pet.objects.all()
    return render(request, 'pets/pet_list.html', {'pets': pets})

@login_required
def pet_detail_auth(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'pets/pet_detail.html', {'pet': pet})
