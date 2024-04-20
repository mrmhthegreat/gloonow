from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib import admin
from django.urls import path,include
from salonbooking.sitemaps import StaticViewSitemap,BookingsSitemap
sitemaps = {
    'static': StaticViewSitemap,
    'bookings': BookingsSitemap
}
urlpatterns = [
     path("", include("salon.urls")),
     path("user/", include("authentication.urls"),name='user'),
       path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name="django.contrib.sitemaps.views.sitemap",),
        path(
        "sitemap-<section>.xml",
       sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
         path("bookings/", include("payment.urls"),name='payment'),
    path('admin/', admin.site.urls),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)