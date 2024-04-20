from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path,include

from payment.views import CancelView,bookings,SuccessView,StripeWebhookView,approveOrreject

urlpatterns = [
 
    path("<slug:slug>/",bookings.as_view(), name="bookings"),
     path("payment/accepts/", approveOrreject, name="approveOrreject"),
     path("payment/success/", SuccessView.as_view(), name="success"),
    path("payment/cancel/", CancelView.as_view(), name="cancel"),
      path("payment/webhooks/stripe/", StripeWebhookView.as_view(), name="stripe-webhook"),
]