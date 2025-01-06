from django.db import models
from pets.models import Pet
from django.contrib.auth.models import User
# Create your models here.

class Activity(models.Model):

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="activities")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    activity = models.CharField(max_length=100)
    date_completed = models.DateTimeField()
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.pet.name} - {self.name} ({self.date_completed})"