import pytest 
from pets.models import Pet
from django.contrib.auth import get_user_model
from activities.views import add_activity, activity_report, edit_activity
from django.http import HttpRequest, QueryDict
from activities.models import Activity
from activities.forms import ActivityForm
from django.utils.timezone import make_aware, get_current_timezone, localtime
from datetime import datetime 
from django.urls import reverse

# function --> Run once per test
# class --> Run once per class
# module --> Run once per module
# session --> Run once per session

@pytest.fixture() 
def set_up(db):
    print('Setting up the user and pet for testing...')
    user = get_user_model().objects.create_user(username='testuser', password='testpass')
    pet = Pet.objects.create(name='Test Pet', user=user, age=1, weight=10)
    return user, pet

class TestAddActivityView:
    def test_add_activity_view_with_form(self, set_up):
        user, pet = set_up
        request = HttpRequest()
        request.user = user
        request.method = 'POST'
        
        # Use QueryDict for request.POST
        post_data = QueryDict(mutable=True)
        post_data.update({
            'activity_name': 'Test Activity',
            'activity_type': 'Walk',
            'date_completed': '2022-01-01',
            'time_completed': '10:00',
            'pet': str(pet.id),  # Pass pet ID as string
            'is_completed': 'true'  # Ensure boolean field is handled correctly
        })
        request.POST = post_data

        # Validate the form before calling the view
        form = ActivityForm(request.POST)
        assert form.is_valid(), form.errors  # Debug form errors

        response = add_activity(request, pet.id)
        assert response.status_code == 302  # Expect redirect

        # Ensure activity is created
        activity = Activity.objects.filter(activity_name='Test Activity').first()
        assert activity is not None, "Activity was not created"
        assert activity.activity_type == 'Walk'
        assert activity.pet == pet  # Ensure pet object matches
        assert activity.is_completed

        # Convert expected datetime to an aware datetime
        expected_datetime = make_aware(datetime.strptime("2022-01-01 10:00", "%Y-%m-%d %H:%M"), get_current_timezone())

        # Ensure date_completed matches (compare using localtime)
        assert localtime(activity.date_completed) == expected_datetime, (
            f"Expected {expected_datetime}, but got {localtime(activity.date_completed)}"
        )

    def test_activity_view_with_invalid_form(self, set_up):
        user, pet = set_up
        request = HttpRequest()
        request.user = user
        request.method = 'POST'
        request.POST = {
            'activity_name': 'Test Activity',
            # Missing required fields should result in a form error 
            'date_completed': '2022-01-01',
            'time_completed': '10:00',
            'pet': str(pet.id),  # Pass pet ID as string
            'is_completed': 'true'  # Ensure boolean field is handled correctly
        }

        response = add_activity(request, pet.id)

        assert response.status_code == 200
        form = ActivityForm(request.POST)
        assert not form.is_valid(), form.errors  # Expect a form error
    
        # Ensure no activity is created
        assert Activity.objects.filter(activity_name='Test Activity').count() == 0

class TestActivityReportView:
    def test_activity_report_view_response(self, set_up):
        user, pet = set_up
        request = HttpRequest()
        request.user = user
        request.method = 'GET'

        response = activity_report(request, pet.id)  
        assert response.status_code == 200

@pytest.mark.django_db
def test_activity_report_view(client, set_up):
    user, pet = set_up
    client.force_login(user)  # Log in the user

    # Create sample activities
    activity1 = Activity.objects.create(
        pet=pet, activity_name="Morning Walk", activity_type="Walk",
        date_completed=make_aware(datetime(2022, 1, 1, 10, 0)), is_completed=True
    )
    activity2 = Activity.objects.create(
        pet=pet, activity_name="Evening Walk", activity_type="Walk",
        date_completed=make_aware(datetime(2022, 1, 2, 18, 0)), is_completed=True
    )
    activity3 = Activity.objects.create(
        pet=pet, activity_name="Vet Visit", activity_type="Vet",
        date_completed=make_aware(datetime(2022, 1, 3, 15, 30)), is_completed=True
    )

    url = reverse('activity_report', args=[pet.id])  # Generate URL for the view

    # **Test 1: No filters applied**
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['activities']) == 3  # Should return all activities

    # **Test 2: Filter by start_date (should exclude activity1)**
    response = client.get(url, {'start_date': '2022-01-02'})
    assert len(response.context['activities']) == 2
    assert activity1 not in response.context['activities']

    # **Test 3: Filter by end_date (should exclude activity3)**
    response = client.get(url, {'end_date': '2022-01-03'})
    assert len(response.context['activities']) == 2
    assert activity3 not in response.context['activities']

    # **Test 4: Filter by activity_type**
    response = client.get(url, {'activity': 'Walk'})
    assert len(response.context['activities']) == 2  # Only walks should appear
    assert all(a.activity_type == 'Walk' for a in response.context['activities'])


       


       






