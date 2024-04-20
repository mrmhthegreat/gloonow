from django.contrib import admin

from glow.models import AppReview,ContactUs,AboutusUs
admin.site.site_header = 'Gloonow'

@admin.register(AppReview)
class appReview_admin(admin.ModelAdmin):
    list_display=['name','email','rating','bid','showin']
    list_filter = ['showin','rating']

    def email(self, obj):
        if(obj.user):
            return obj.user.email 


        return 'No ' 
      #Allows column order sorting
    email.short_description = 'By Email' 

    def name(self, obj):
        if(obj.user):
            return obj.user.first_name 


        return 'No ' 
      #Allows column order sorting
    name.short_description = 'By Name' 
@admin.register(ContactUs)
class contactUs_admin(admin.ModelAdmin):
    list_display=['first_name','email','subject']
  
    search_fields = ["email",'first_name']
   
@admin.register(AboutusUs)
class aboutUs_admin(admin.ModelAdmin):
    list_display=['company','email','address']