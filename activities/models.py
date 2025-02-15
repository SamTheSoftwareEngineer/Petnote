from django.db import models
from pets.models import Pet
from django.conf import settings
# Create your models here.

class Activity(models.Model):
    ACTIVITY_CHOICES = [
        ("Walk", "Walk"),
        ("Play", "Play"),
        ("Feed", "Feed"),
        ("Vet", "Vet"),
        ("Groom", "Groom"),
        ("Training", "Training"),
        ("Medicine", "Medicine"),
        ("Other", "Other"),
    ]

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="activities")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    activity_name = models.CharField(max_length=100, default="")
    activity_type = models.CharField(max_length=100, choices=ACTIVITY_CHOICES, default='Select Activity')
    activity = models.CharField(max_length=100)
    date_completed = models.DateTimeField()
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.pet.name} - {self.activity_name} ({self.date_completed})"