from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.
class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to="profile_pictures", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

PET_TYPES = (
    ("Dog", "Dog"),
    ("Cat", "Cat"),
    ("Bird", "Bird"),
    ("Fish", "Fish"),
    ("Reptile", "Reptile"),
    ("Amphibian", "Amphibian"),
    ('small animal, Small Animal'),
    ("Other", "Other"),
)

class Pet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=100, choices=PET_TYPES)
    age = models.IntegerField()
    pet_profile_picture = models.ImageField(upload_to="pet_profile_pictures", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

ACTIVITY_TYPES = (
    ("walking", "Walking"),
    ("running", "Running"),
    ("swimming", "Swimming"),
    ("Playing", "playing")
    ("Feeding", "feeding"),
    ("Grooming", "grooming"),
    ("medication", "Medication"),
    ("other", "Other"),
)

class Activity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100, choices=ACTIVITY_TYPES)
    start_time = models.DateTimeField(blank=True, null=True)
    end_timee = models.DateTimeField(blank=True, null=True)