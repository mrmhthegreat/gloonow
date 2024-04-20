from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from salon.models import BookingPost
class StaticViewSitemap(Sitemap):
    def items(self):
        return ['about','terms','contactus']
    def location(self, item):
        return reverse(item)
    
    
class BookingsSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    def items(self):
        return BookingPost.objects.search().order_by("-user__rating")
    def lastmod(self, obj):
        return obj.date_posted