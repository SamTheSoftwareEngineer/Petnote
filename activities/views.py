
from django.shortcuts import render, get_object_or_404, redirect
from .models import Activity
from .forms import ActivityForm
from pets.models import Pet
from django.contrib.auth.decorators import login_required
from datetime import datetime 
from django.utils.timezone import make_aware, get_current_timezone
from django.db.models import Count 

@login_required
def add_activity(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == "POST":
        form = ActivityForm(request.POST)
        if form.is_valid():
            # Extract the date and time from the form
            date_completed = request.POST.get('date_completed')
            time_completed = request.POST.get('time_completed')

            # Check if both date and time are provided
            if date_completed and time_completed:
                # Combine date and time into a single datetime object
                naive_datetime = datetime.strptime(f"{date_completed} {time_completed}", "%Y-%m-%d %H:%M")

                # Convert to aware datetime
                aware_datetime = make_aware(naive_datetime, get_current_timezone())
                # Save the activity with the combined datetime to the database
                activity = form.save(commit=False)
                activity.date_completed = aware_datetime
                activity.pet = pet  # Assign the pet to the activity    

                print('Saving activity...')
                activity.save()
                print('Activity saved! Redirecting...')

                # Redirect to the pet detail page
                return redirect('pet_detail', pet_id=pet_id) 
            else:
                # If either date or time is missing, show an error message
                form.add_error('date_completed', "Please provide both date and time.")        
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

@login_required
def toggle_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    activity.completed = not activity.completed
    activity.save()
    return redirect('pet_detail', pet_id=activity.pet.id)

@login_required
def activity_report(request, pet_id):
    # Grab the pet object
    pet = get_object_or_404(Pet, id=pet_id)

    # Get all activities for the pet
    activities = Activity.objects.filter(pet=pet)

    # Apply filtering (if the user entered filters)

    # Fetch start_date and end_date from GET parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Initialize the activities queryset
    activities = pet.activities.all()

    # Parse and apply date filters if provided
    if start_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            activities = activities.filter(date_completed__gte=start_date)
        except ValueError:
            start_date = None 
    if end_date:
        try:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            activities = activities.filter(date_completed__lte=end_date)
        except ValueError:
            end_date = None  
    
    # TODO: Apply activity filter if provided
    activity_type = request.GET.get('activity')
    if activity_type:
        activities = activities.filter(activity_type=activity_type)

    # Generate a summary grouped by activity type
    summary = activities.values('activity').annotate(total=Count('id'))

    return render(request, 'activity_report.html', 
                  {'pet': pet, 
                   'summary': summary, 
                   'activities': activities,
                   'start_date': start_date,
                   'end_date': end_date,
                   'ACTIVITY_CHOICES': Activity.ACTIVITY_CHOICES,
                   })
                