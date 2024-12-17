from django.urls import path
from . import views

urlpatterns = [
    path('', views.pet_list, name='pet_list'),
]