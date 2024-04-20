from django.urls import path

from . import views

urlpatterns = [
    path("posts", views.PostListView.as_view(), name="postlist"),
    path("", views.index, name="index"),
    path("terms/", views.terms, name="terms"),
    path("about/", views.about, name="about"),
    path("contactus/", views.contactus, name="contactus"),
    path("dashboard/", views.dashboarrd, name="dashboard"),
    path("dashboard/mypost/", views.mybookings.as_view(), name="mybookings"),
    path("dashboard/mybooking/", views.mybooking.as_view(), name="mybooking"),
    path("createpost/", views.createPost.as_view(), name="createpost"),
    path("booking/getimese/", views.getimese, name="getimese"),
    path("booking/deactivate/", views.deactive, name="deactivate"),
    path("booking/cancelbook/", views.canclebook, name="canclebook"),
    path("booking/addreview/", views.addreviesw, name="addreviews"),
    path("dashboard/allreviews/", views.allreviews.as_view(), name="allreviews"),


]