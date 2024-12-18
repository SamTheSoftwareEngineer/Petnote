from django.shortcuts import render, redirect, get_object_or_404
from .models import Pet
from .forms import PetForm

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