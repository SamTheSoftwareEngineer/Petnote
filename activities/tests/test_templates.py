import pytest
from pets.models import Pet
from activities.forms import ActivityForm
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.http import HttpRequest
from activities.models import Activity
from django.utils import timezone
from datetime import datetime

naive_date = datetime(2022, 1, 1)
aware_date = timezone.make_aware(naive_date, timezone.get_current_timezone())

"""Contains tests for the templates and forms in the activities app."""

@pytest.fixture
def user(db):
    return get_user_model().objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def pet(user, db):
    return Pet.objects.create(name='Test Pet', user=user, age=1, weight=10)

@pytest.mark.django_db
def test_add_activity_template(user, pet):
    # Use the user and pet fixtures to create a test user and pet
    user = user
    pet = pet

    # Create a dummy request object
    request = HttpRequest()
    request.user = user

    # Render the add_activity template with the user and pet fixtures
    response = render_to_string('add_activity.html', {'form': ActivityForm(), 'pet': pet}, request=request)

    # Check that the template was rendered successfully
    assert response is not None 
    # Check that the form is in the context
    assert 'form' in response

    # Check that the pet is in the context
    assert 'pet' in response

@pytest.mark.django_db
def test_edit_activity_template(user, pet):
    # Use the user and pet fixtures to create a test user and pet
    user = user
    pet = pet

    # Create a dummy request object
    request = HttpRequest()
    request.user = user

    # Create a dummy activity
    activity = Activity.objects.create(
        pet=pet,
        user=user,
        activity_name='Test Activity',
        date_completed=aware_date
    )

    # Render the add_activity template with the user and pet fixtures
    response = render_to_string('edit_activity.html', {'form': ActivityForm(instance=activity), 'pet': pet, 'activity': activity}, request=request)

    # Check that the template was rendered successfully
    assert response is not None 
    # Check that the form is in the context
    assert 'form' in response

    # Check that the pet is in the context
    assert 'pet' in response

@pytest.mark.django_db
def test_activity_report_template(user, pet):
    # Use the user and pet fixtures to create a test user and pet
    user = user
    pet = pet

    # Create a dummy request object
    request = HttpRequest()
    request.user = user

    # Render the add_activity template with the user and pet fixtures
    response = render_to_string('activity_report.html', {'form': ActivityForm(), 'pet': pet, 'ACTIVITY_CHOICES': Activity.ACTIVITY_CHOICES}, request=request)

    # Check that the template was rendered successfully
    assert response is not None 
    # Check that the form is in the context
    assert 'form' in response

    # Check that the pet is in the context
    assert 'pet' in response

    