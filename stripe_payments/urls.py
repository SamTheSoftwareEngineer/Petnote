from django.urls import path, include 
from . import views

urlpatterns = [
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
    path("pricing-page/", views.pricing_page, name="pricing_page"),
    path("subscription-confirm/", views.subscription_confirm, name="subscription_confirm"),
    path("webhook/", views.stripe_webhook, name="webhook"),
]