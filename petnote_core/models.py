from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=250, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=250, blank=True, null=True)
    is_subscribed = models.BooleanField(default=False)
    class Meta:
        db_table = 'petnote_core_customuser'

class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(("email address"), max_length=254, unique=True, blank=False)
    image = models.ImageField(upload_to='profile_images', blank=True)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
     
