
from django.urls import path
from . import views

urlpatterns = [
    path('<int:pet_id>/add/', views.add_activity, name='add_activity'), # Correct URL
    path('edit/<int:pk>/', views.edit_activity, name='edit_activity'),
    path('delete/<int:activity_id>/', views.delete_activity, name='delete_activity'),
]
