from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/logout/', views.logout_view, name='logout'),
]



