from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Pet(models.Model):
    photo = models.ImageField(upload_to='pet_photos', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    age = models.IntegerField()
    weight = models.IntegerField()
    breed = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name
    
