import sendgrid
import os 
from django.core.signing import TimestampSigner, BadSignature
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, UpdateUsernameForm, UserCreationForm
from pets.models import Pet
from sendgrid.helpers.mail import Mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.http import HttpResponse


def index(request):
    # Check if the user is authenticated and redirect to the pet page 
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        # If the user is not authenticated, render the index template
        return render(request, 'core/index.html')

@login_required
def profile_view(request):
    profile = request.user.userprofile
    pets_count = Pet.objects.filter(user=request.user).count()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    context = {
        'form': form,
        'pets': pets_count,
        'profile': profile,
        'pets_count': pets_count
    }
    return render(request, 'core/profile.html', context)

# Initialize signer for email verification tokens
signer = TimestampSigner()

def generate_token(user):
    """Generates a secure verification token."""
    return signer.sign(user.id)

# Load SendGrid API credentials and dynamic template from environment
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
VERIFICATION_TEMPLATE_ID = os.environ.get('VERIFICATION_TEMPLATE_ID')

def send_verification_email(request, user):
    """Sends a verification email to the user upon registration using SendGrid."""
    user = User.objects.create(username=user.username, email=user.email, is_active=False)
    user.refresh_from_db()  # Ensures the user has an ID from the database
    token = generate_token(user)  
    domain = get_current_site(request).domain
    verify_url = f"http://{domain}{reverse('verify_email', kwargs={'token': token})}"

    message = Mail(
        from_email="contact@mypetnote.com",
        to_emails=user.email,
    )
    message.template_id = VERIFICATION_TEMPLATE_ID

    # Pass dynamic data to SendGrid template
    message.dynamic_template_data = {
        "username": user.username,
        "verify_url": verify_url
    }

    try:
        sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
    except Exception as e:
        print(f"Error sending message: {str(e)}")

def verify_email(request, token):
    """Handles email verification when the user clicks the link."""
    try:
        if not token:
            return HttpResponse("Invalid token provided.")
        else:
            user_id = signer.unsign(token, max_age=86400)  # Token expires after 1 day
            user = get_object_or_404(User, id=user_id)
            user.is_active = True  # Activate account
            user.save()
            return render(request, 'core/verification_success.html')
    except BadSignature:
        # Render a custom error page with a friendly message
        error_message = "The verification link is invalid or has expired. Please request a new verification email."
        return render(request, 'core/token_expired.html', {'error_message': error_message})

def signup(request):
    """Handles user registration and sends a verification email."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set inactive until email verification is sent

            # Check to make sure that the email is not already in use 
            if User.objects.filter(email=user.email).exists():
                form.add_error('email', 'This email address is already in use.')
                return render(request, 'core/signup.html', {'form': form})  
            
            send_verification_email(request, user)  # Send verification email
            
            return render(request, 'core/verification_sent.html')
    else:
        form = UserCreationForm()
    
    return render(request, 'core/signup.html', {'form': form})

def verification_sent(request):
    return render(request, 'core/verification_sent.html')

def thanks_view(request):
    return render(request, 'core/thanks.html')

@login_required
def update_username(request):
    if request.method == 'POST':
        form = UpdateUsernameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()  # Save the updated username
            return redirect('profile')  # Redirect to the user's profile page 
    else:
        form = UpdateUsernameForm(instance=request.user)

    return render(request, 'core/update_username.html', {'form': form})

