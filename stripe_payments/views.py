from django.shortcuts import render, redirect
from django.conf import settings
from djstripe.settings import djstripe_settings
from djstripe.models import Subscription, Customer
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import get_user_model
import stripe
import json
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@login_required
def pricing_page(request):
    return render(request, 'pricing_page.html', {
        'stripe_public_key': djstripe_settings.STRIPE_PUBLIC_KEY,
        'stripe_pricing_table_id': settings.STRIPE_PRICING_TABLE_ID,
    })


@login_required
def subscription_confirm(request):
    # Configure our stripe API keys
    stripe.api_key = djstripe_settings.STRIPE_SECRET_KEY

    # Get the session id from the URL
    session_id = request.GET.get("session_id")

    if not session_id:
        messages.error(request, "Missing session ID. Please contact support.")
        return HttpResponseRedirect(reverse("pricing_page"))

    print(f"Session ID received: {session_id}")  # Debugging log

    # Retrieve the session object from Stripe
    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except stripe.error.InvalidRequestError:
        messages.error(request, "Invalid session ID. Please try again.")
        return HttpResponseRedirect(reverse("pricing_page"))

    # Get the subscribing user object from the client_reference_id
    client_reference_id = session.client_reference_id
    if not client_reference_id:
        messages.error(request, "Invalid client reference ID.")
        return HttpResponseRedirect(reverse("pricing_page"))

    try:
        subscription_holder = get_user_model().objects.get(id=int(client_reference_id))
    except get_user_model().DoesNotExist:
        messages.error(request, "User with provided ID not found.")
        return HttpResponseRedirect(reverse("pricing_page"))
    except ValueError:
        messages.error(request, "Invalid client reference ID format.")
        return HttpResponseRedirect(reverse("pricing_page"))

    # Sanity check that the logged-in user matches
    if subscription_holder != request.user:
        messages.error(request, "Unauthorized request.")
        return HttpResponseRedirect(reverse("pricing_page"))

    # Retrieve subscription object from Stripe
    try:
        subscription = stripe.Subscription.retrieve(session.subscription)
    except stripe.error.InvalidRequestError:
        messages.error(request, "Could not retrieve subscription from Stripe.  Please contact support.")
        return HttpResponseRedirect(reverse("pricing_page"))

    djstripe_subscription = Subscription.sync_from_stripe_data(subscription)

    # Set the subscription and customer on the user
    subscription_holder.subscription = djstripe_subscription

    # Ensure the user has a djstripe Customer object
    if not hasattr(subscription_holder, 'customer') or subscription_holder.customer is None:
        customer = Customer.sync_from_stripe_data(stripe.Customer.retrieve(session.customer))
        subscription_holder.customer = customer
    
    subscription_holder.save()

    messages.success(request, "You have successfully subscribed to PetNote! Thanks for the support!")
    return render(request, 'subscription_confirmation.html', {'session_id': session_id})


@login_required
@require_POST
def create_portal_session(request):
    stripe.api_key = djstripe_settings.STRIPE_SECRET_KEY
    portal_session = stripe.billing_portal.Session.create(
        customer=request.user.customer.stripe_id,
        return_url="http://localhost:8000/subscription-details/",
    )
    return HttpResponseRedirect(portal_session.url)

# Webhook for Stripe to handle subscription updates

endpoint_secret = settings.DJSTRIPE_WEBHOOK_SECRET

def handle_payment_intent_succeeded(payment_intent):
    # Update your database to reflect the successful payment
    # Send a notification to the customer
    print(f'Payment intent {payment_intent["id"]} succeeded')

def handle_payment_method_attached(payment_method):
    # Update your database to reflect the attached payment method
    # Send a notification to the customer
    print(f'Payment method {payment_method["id"]} attached')

@require_POST
@csrf_exempt
def stripe_webhook(request):
    # Read event data
    event = None
    payload = request.body

    try:
        event = json.loads(payload)
    except json.decoder.JSONDecodeError as e:
        print('- ERROR: Invalid payload: %s' % e)
        return JsonResponse({'success': False})
    
    if endpoint_secret:
        # Only verify the event if there is an endpoint secret defined
        # otherwise use the basic event deserialization
        sig_header = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except stripe.error.SignatureVerificationError as e:
            # Invalid payload
            print('- ERROR: Webhook signature verification failed: %s' % e)
            return JsonResponse({'success': False})
        
    # Handle the event
    if event and event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        print(f' Payment for {payment_intent["amount"]} succeeded')

        # Then define and call a method to handle the successful payment intent.
        # handle_payment_intent_succeeded(payment_intent)

    elif event and event['type'] == 'payment_method.attached':
        payment_method = event['data']['object']  # contains a stripe.PaymentMethod
        print(f' PaymentMethod {payment_method["id"]} attached to customer {payment_method["customer"]}')

        # Then define and call a method to handle the successful attachment of a PaymentMethod.
        # handle_payment_method_attached(payment_method)
    
    elif event and event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        print(f' Payment for {payment_intent["amount"]} succeeded')
        handle_payment_intent_succeeded(payment_intent)
    
    elif event and event['type'] == 'payment_method.attached':
        payment_method = event['data']['object']  # contains a stripe.PaymentMethod
        print(f'PaymentMethod {payment_method["id"]} attached to customer {payment_method["customer"]}')
        handle_payment_method_attached(payment_method)

    else:
        # Unexpected event type
        print('Received unknown event type {}.'.format(event['type']))

    return JsonResponse({'success': True})