from django.urls import path

from . import views

urlpatterns = [
    # Home page 
    path('', views.index, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('thanks/', views.thanks_view, name='thanks'),
]



