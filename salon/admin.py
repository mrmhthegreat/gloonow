from django.contrib import admin

from salon.models import BookingPost,Services,BookBy,SaloonReview

@admin.register(SaloonReview)
class wallet_admin(admin.ModelAdmin):
    list_display=['name','email','saloonname','rating']
    list_filter = ['saloon','rating']
    search_fields = ['rating',]

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
    def saloonname(self, obj):
        if(obj.user):
            return obj.saloon.company 


        return 'No ' 
      #Allows column order sorting
    saloonname.short_description = 'To Saloon' 
@admin.register(BookingPost)
class post_admin(admin.ModelAdmin):
    list_display=['slug','is_active','useremail']
    readonly_fields = ["slug"]
    list_filter = ['is_active','services']
    search_fields = ['title','services__name','user__company','user__email']

    def useremail(self, obj):
        if(obj.user):
            return obj.user.email 


        return 'No ' 
      #Allows column order sorting
    useremail.short_description = 'useremail' 
@admin.register(Services)
class ser_admin(admin.ModelAdmin):
    list_display=['name','perority']
    search_fields = ['name']

@admin.register(BookBy)
class bookby_admin(admin.ModelAdmin):
    list_display=['name','email','salonname','salonemail','time','payment','confirm','reject','cancle']
    list_filter = ['confirm','payment','cancle','is_active','saloon__company','reject']
    search_fields = ['slug']
    def name(self, obj):
        if(obj.user):
            return obj.user.first_name 


        return 'No ' 
      #Allows column order sorting
    name.short_description = 'By' 
    def email(self, obj):
        if(obj.user):
            return obj.user.email 


        return 'No ' 
      #Allows column order sorting
    email.short_description = 'Email'
    def salonname(self, obj):
        if(obj.user):
            return obj.saloon.company 


        return 'No ' 
      #Allows column order sorting
    salonname.short_description = 'From' 
    def salonemail(self, obj):
        if(obj.user):
            return obj.saloon.email 


        return 'No ' 
      #Allows column order sorting
    salonemail.short_description = 'Email' 