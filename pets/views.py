from django.shortcuts import render
from .models import Pet
# Create your views here.

def pet_list(request):
    pets = Pet.objects.all() # get all pets 
    return render(request, 'pets/pet_list.html', {'pets': pets})
