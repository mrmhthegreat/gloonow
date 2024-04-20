from django.contrib import admin

# Register your models here.
from payment.models import Price,Payment,Wallet


@admin.register(Wallet)
class wallet_admin(admin.ModelAdmin):
    list_display=['name','email','amount']
   
    def email(self, obj):
        if(obj.user):
            return obj.user.email 


        return 'No ' 
      #Allows column order sorting
    email.short_description = 'Email' 

    def name(self, obj):
        if(obj.user):
            return obj.user.first_name 


        return 'No ' 
      #Allows column order sorting
    name.short_description = 'Name' 

admin.site.register(Price)
@admin.register(Payment)
class payment_admin(admin.ModelAdmin):
    list_display=['name','email','price',"payment_status","salon",'bookingid']
    readonly_fields = ['name','email','price',"payment_status","user",'book_id','payment_id']
    list_filter = ['payment_status','book_id__saloon__company']
    search_fields = ['payment_id']
    def email(self, obj):
        if(obj.user):
            return obj.user.email 


        return 'No ' 
      #Allows column order sorting
    email.short_description = 'Email' 

    def name(self, obj):
        if(obj.user):
            return obj.user.first_name 


        return 'No ' 
      #Allows column order sorting
    name.short_description = 'Name'
    def salon(self, obj):
        if(obj.user):
            return obj.book_id.user.company 


        return 'No ' 
      #Allows column order sorting
    salon.short_description = 'Saloon'
    def bookingid(self, obj):
        if(obj.user):
            return obj.book_id.payment_id


        return 'No ' 
      #Allows column order sorting
    bookingid.short_description = 'Booking id'