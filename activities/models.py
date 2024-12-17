from django.db import models
from pets.models import Pet
# Create your models here.

class Activity(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    activity = models.CharField(max_length=100)
    date_completed = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)