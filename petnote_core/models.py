from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to='profile_images', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'petnote_core_customuser'

class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(("email address"), max_length=254, unique=True, blank=False)
    image = models.ImageField(upload_to='profile_images', blank=True)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
     
