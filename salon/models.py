
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from authentication.models import UserProfile,Region,SaloonTypes
from django.db.models import Q
from django.urls import reverse
from datetime import datetime,timedelta

class Services(models.Model):
    name = models.CharField(max_length=255)
   
    perority = models.IntegerField( default=0,null=False,blank=False)
    class Meta:
        ordering = ['-perority']
    def __str__(self):
        return self.name

    def __str__(self):
        return self.name
class TimeAdvance(models.Model):
    name = models.CharField(max_length=255)
    starttime=models.TimeField(null=True)
    endtime=models.TimeField(null=True)
    perority = models.IntegerField( default=0,null=False,blank=False)
    class Meta:
        ordering = ['-perority']
    def __str__(self):
        return self.name
class BookingPostQuerySet(models.QuerySet):
    def is_active(self):
        return self.filter(is_active=False)
    def search(self,active=True):
        current_time = datetime.now().replace(second=0, microsecond=0)
        
        v=current_time-timedelta(days = 1)
        
        lookup=Q(bookdatetime__gte=current_time)&Q(is_active=True)&Q(is_hide=False)&Q(is_book=False)
        
        qs=self.filter(lookup)
            
        return qs.distinct()
          
    def search2(self,type,active=True):
        current_time = datetime.now().replace(second=0, microsecond=0)
        
        v=current_time-timedelta(days = 1)
        lookup=Q(user__type__name=type.name)&Q(bookdatetime__gte=current_time)&Q(is_active=True)&Q(is_hide=False)&Q(is_book=False)
        
        qs=self.filter(lookup)
            
        return qs.distinct() 
    def filterspecfice(self,date,services,regions,type,active=True):
        if type!=None:

            lookup=Q(user__region__name=regions.name)&Q(user__type__name=type.name)&Q(bookdate=date)&Q(services__in=[x.id for x in services])&Q(is_active=True)&Q(is_hide=False)&Q(is_book=False)
        else:
            lookup=Q(user__region__name=regions.name)&Q(bookdate=date)&Q(services__in=[x.id for x in services])&Q(is_active=True)&Q(is_hide=False)&Q(is_book=False)

        qs=self.filter(lookup)
            
        return qs.distinct()
     
    def filterspecficesv(self,services,regions,type, active=True):
        current_time = datetime.now().replace(second=0, microsecond=0)
        if type!=None:

            lookup= Q(user__region__name=regions.name)&Q(user__type__name=type.name)&Q(bookdatetime__gte=current_time)&Q(services__in=[x.id for x in services])&Q(is_active=True)&Q(is_hide=False)&Q(is_book=False)
        else:
            lookup= Q(user__region__name=regions.name)&Q(bookdatetime__gte=current_time)&Q(services__in=[x.id for x in services])&Q(is_active=True)&Q(is_hide=False)&Q(is_book=False)

        
        qs=self.filter(lookup)
            
        return qs.distinct()
    def filterdatespecficesv(self,services,regions,type,active=True):
        current_time = datetime.now().replace(second=0, microsecond=0,day=services.day,year=services.year,month=services.month)
        if type!=None:

            lookup=Q(user__region__name=regions.name)&Q(user__type__name=type.name)&Q(bookdate=services)&Q(bookdatetime__gte=current_time)&Q(is_active=True)&Q(is_hide=False)&Q(is_book=False)
        else:
            lookup=Q(user__region__name=regions.name)&Q(bookdate=services)&Q(bookdatetime__gte=current_time)&Q(is_active=True)&Q(is_hide=False)&Q(is_book=False)

        qs=self.filter(lookup)
            
        return qs.distinct()
        
class BookingPostManger(models.Manager):
    def get_queryset(self,*args,**kwrgs):
        
        return BookingPostQuerySet(self.model,using=self._db)

    def search(self,active=True):
        return self.get_queryset().search(active=active)
    def search2(self,type,active=True):
        return self.get_queryset().search2(type,active=active)
    def filterspecfice(self,query,services,region,type,active=True):
        return self.get_queryset().filterspecfice(query,services,region,type,active=active)
    def filterspecficesv(self,services,region,type,active=True):
        return self.get_queryset().filterspecficesv(services,region,type,active=active)
    def filterdatespecficesv(self,services,region,type,active=True):
        return self.get_queryset().filterdatespecficesv(services,region,type,active=active)
class BookingPost(models.Model):
    slug=models.SlugField(blank=True,null=True,unique=True,max_length=1000)
    services=models.ManyToManyField(Services,blank=True)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    title=models.CharField(max_length=120, null=True,blank=True,default='')
    message=models.TextField(max_length=5000, null=True,blank=True,default='')
    image = models.ImageField(blank=True,upload_to='media/post/',null=True)
    address = models.CharField(max_length=120,null=True,blank=True, default='')
    extra = models.JSONField(null=True,)
    phone_number = PhoneNumberField(blank=True,help_text="0064xxxxxxx format",region="NZ",error_messages={'invalid':"please reenter your number in 0064xxxxxxxxx format – e.g. 0064217774444"})
    is_active=models.BooleanField(default=False)
    is_book=models.BooleanField(default=False)
    is_hide=models.BooleanField(default=False)
    date_create=models.DateField(auto_now=True)
    bookdatetime=models.DateTimeField(null=True)
    bookdate=models.DateField(null=True)
    booktime=models.TimeField(null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    objects=BookingPostManger()

    class Meta:
        ordering = ['-date_posted']
    def __str__(self):
        return self.question
    def get_absolute_url(self):
        return reverse('bookings', kwargs={'slug': self.slug},)

 
    def __str__(self):
        return self.slug


class SaloonReview(models.Model):
    rating = models.DecimalField(max_digits=2, null=True,blank=True,decimal_places=1)
    message=models.TextField(max_length=5000, null=True,blank=True,default='')
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="userreview")
    saloon = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="saloonreview")
    date_create=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} Give {self.rating} To {self.saloon.company}"
class AdvanceRequest(models.Model):
    slug=models.SlugField(blank=True,null=True,unique=True,max_length=1000)
    services=models.ManyToManyField(Services,blank=True)
    email=models.EmailField(max_length=120, null=True,blank=True,default='')
    name=models.CharField(max_length=220, null=True,blank=True,default='')
    times=models.ManyToManyField(TimeAdvance,blank=True)
    extra = models.JSONField(null=True,)
    sended=models.BooleanField(default=False)
    region=models.ForeignKey(Region,null=True,blank=True,on_delete=models.CASCADE)
    salontype=models.ForeignKey(SaloonTypes,null=True,blank=True,on_delete=models.CASCADE)

    date_create=models.DateField(auto_now_add=True)


    def __str__(self):
        return self.slug
    
 
    def __str__(self):
        return self.slug 

class BookBy(models.Model):
    slug=models.SlugField(blank=True,null=True,unique=True,max_length=1000)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="user")
    saloon = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="saloon")
    booking=models.ForeignKey(BookingPost,on_delete=models.CASCADE,)
    services=models.ManyToManyField(Services,blank=True)
    payment=models.BooleanField(default=False)
    cancle=models.BooleanField(default=False)
    confirm=models.BooleanField(default=False)
    reject=models.BooleanField(default=False)
    done=models.BooleanField(default=False)
    hideforowner=models.BooleanField(default=False)
    hideforuser=models.BooleanField(default=False)
    cancle_reason=models.CharField(max_length=5000, null=True,blank=True,default='')
    payment_id=models.CharField(max_length=5000, null=True,blank=True,default='')
    message=models.TextField(max_length=5000, null=True,blank=True,default='')
    address = models.CharField(max_length=120,null=True,blank=True, default='')
    time = models.CharField(max_length=120,null=True,blank=True, default='')
    date = models.CharField(max_length=120,null=True,blank=True, default='')
    extra = models.JSONField(null=True,)
    phone_number = PhoneNumberField(blank=True,help_text="0064xxxxxxx format",region="NZ",error_messages={'invalid':"please reenter your number in 0064xxxxxxxxx format – e.g. 0064217774444"})
    is_active=models.BooleanField(default=False)
    date_create=models.DateField(auto_now_add=True)
    price = models.DecimalField(decimal_places=2, max_digits=10,default=40)

    class Meta:
        ordering = ['-date_create']
    def __str__(self):
        return self.question
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug},)

 
    def __str__(self):
        return self.slug
    





