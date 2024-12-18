from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # User registration
    path('signup/', views.signup, name='signup'),
    # Login
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    # Logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
