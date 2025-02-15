from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home page 
    path('', views.index, name='home'),
    # User profile
    path('profile/', views.profile_view, name='profile'),
    # Signup
    path('signup/', views.signup, name='signup'),
    # Login
    path('login/', auth_views.LoginView.as_view(), name='login'),
    # Logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Thanks
    path('thanks/', views.thanks_view, name='thanks'),
    # Update username
    path('update-username/', views.update_username, name='update_username'),
    # Password changes
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='core/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='core/password_change_done.html'), name='password_change_done'),
    # Password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='core/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'), name='password_reset_complete'),

    
]



