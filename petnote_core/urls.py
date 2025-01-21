from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    # User profile
    path('profile/', views.profile_view, name='profile'),
    # User registration
    path('signup/', views.signup, name='signup'),
    # Login
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', next_page='profile'), name='login'),
    # Logout
    path('logout/', auth_views.LogoutView.as_view(next_page='thanks'), name='logout'),
    # Thanks
    path('thanks/', views.thanks_view, name='thanks'),
    # Update username
    path('update-username/', views.update_username, name='update_username'),
    # Reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='core/password_reset.html'), name='password_reset'),
    # Password reset done
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'), name='password_reset_done'),
    # Password reset confirm
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset_confirm.html'), name='password_reset_confirm'),
    # Password reset complete
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'), name='password_reset_complete'),
]
