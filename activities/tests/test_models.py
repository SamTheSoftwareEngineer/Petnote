import pytest
from activities.models import Activity
from django.contrib.auth import get_user_model
from pets.models import Pet
from datetime import date
from django.utils import timezone
import datetime

naive_date = datetime.datetime(2022, 1, 1)
aware_date = timezone.make_aware(naive_date, timezone.get_current_timezone())

# Fixture to create a user
@pytest.fixture
def user(db):  # db fixture ensures database access
    return get_user_model().objects.create_user(username='testuser', password='testpass')

# Fixture to create a pet
@pytest.fixture
def pet(user, db):  # user fixture ensures user exists before creating a pet
    return Pet.objects.create(name='Test Pet', user=user, age=1, weight=10)

# Test string representation of Activity
@pytest.mark.django_db
def test_activity_str(user, pet):
    activity = Activity.objects.create(
        pet=pet,
        user=user,
        activity='Test Activity',
        activity_name='Test Activity Name',
        activity_type='Walk',
        date_completed=date(2022, 1, 1),  # Use a `date` object
    )
    assert str(activity) == 'Test Pet - Test Activity Name (2022-01-01)'

# Test activity type choices
def test_activity_type_choices():
    assert Activity.ACTIVITY_CHOICES == [
        ('Walk', 'Walk'),
        ('Play', 'Play'),
        ('Feed', 'Feed'),
        ('Vet', 'Vet'),
        ('Groom', 'Groom'),
        ('Training', 'Training'),
        ('Medicine', 'Medicine'),
        ('Other', 'Other'),
    ]

# Test date_completed formatting
@pytest.mark.django_db
def test_date_completed_format():
    activity = Activity(date_completed=aware_date)
    assert activity.date_completed.strftime('%Y-%m-%d') == '2022-01-01'


# Test pet relationship
@pytest.mark.django_db
def test_pet_relationship(user, pet):
    activity = Activity.objects.create(
        pet=pet,
        user=user,
        activity_name='Test Activity',
        date_completed=aware_date
    )
    assert activity.pet == pet

# Test user relationship
@pytest.mark.django_db
def test_user_relationship(user, pet):
    activity = Activity.objects.create(
        pet=pet,
        user=user,
        activity_name='Test Activity',
        date_completed=aware_date,
    )
    assert activity.user == user
