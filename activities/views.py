
from django.shortcuts import render, get_object_or_404, redirect
from .models import Activity
from .forms import ActivityForm
from pets.models import Pet


def add_activity(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == "POST":
        form = ActivityForm(request.POST)
        if form.is_valid():
            # Save the new activity
            activity = form.save(commit=False)
            print('Saving activity...')
            activity.pet = pet  # Assign the pet to the activity
            print('Assigning pet to activity...')
            activity.save()
            print('Activity saved! Redirecting...')

            # Redirect to the pet detail page
            return redirect('pet_detail', pet_id=pet_id) 
        else: 
            print("Form errors:", form.errors)

    else:
        # If the request method is GET, create an empty form
        form = ActivityForm()

    return render(request,'add_activity.html', {
        'form': form,
        'pet': pet
    })

def edit_activity(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == "POST":
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('pet_detail', pet_id=activity.pet.id)
    else:
        form = ActivityForm(instance=activity)
    return render(request, 'edit_activity.html', {'form': form, 'activity': activity})

def delete_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    pet_id = activity.pet.id  # Save the pet ID before deleting
    activity.delete()
    return redirect('pet_detail', pet_id=pet_id)  # Redirect back to the pet detail page
