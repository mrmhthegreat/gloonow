from django.urls import path

from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path("login/", views.signin.as_view(), name="singin"),
    path("restpassword/", views.forgortpassword.as_view(), name="forgortpassword"),
    path("passwordrestdone/", views.passwordRestDone.as_view(), name="passwordrestdone"),
    path("passwordrestconfirm/<uidb64>/<token>/", views.passwordRestconfirm.as_view(), name="password-reset-confirm"),
    path("logout/", views.logout_view, name="logout"),
    path("registration/", views.signup.as_view(), name="singup"),
    path("salonregistration/", views.owner.as_view(), name="owner"),
    path("dashboard/update/", views.userUpdateView.as_view(), name="update"),
    path("dashboard/changepassword/", views.changepassword.as_view(), name="changepassword"),
     path('verify-email/', views.verify_email, name='verify-email'),
    path('verify-email/done/', views.verify_email_done, name='verify-email-done'),
    path('verify-email-confirm/<uidb64>/<token>/', views.verify_email_confirm, name='verify-email-confirm'),
    path('verify-email/complete/', views.verify_email_complete, name='verify-email-complete'),
]