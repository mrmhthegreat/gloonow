from django.db import models
from authentication.models import UserProfile
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class AppReview(models.Model):
    rating = models.DecimalField(max_digits=2, null=True,blank=True,decimal_places=1)
    bid = models.IntegerField(null=True,blank=True,default=0)
    message=models.TextField(max_length=5000, null=True,blank=True,default='')
    showin=models.BooleanField(default=False, null=True,blank=True,)
    user = models.OneToOneField(UserProfile,on_delete=models.CASCADE,related_name='reviews')
    date_create=models.DateField(auto_now_add=True)
    class Meta:
        ordering = ['-rating','-date_create']
    def __str__(self):
        return f"{self.user.first_name} Give {self.rating} To Web "

class ContactUs(models.Model):
    subject=models.CharField(max_length=5000, null=True,blank=True,default='')
    message=models.TextField(max_length=5000, null=True,blank=True,default='')
    email=models.EmailField(max_length=255, null=True,blank=True,default='')
    
    phone_number = PhoneNumberField(blank=True, unique=True,region="NZ",help_text="0064xxxxxxx format",error_messages={'invalid':"please reenter your number in 0064xxxxxxxxx format – e.g. 0064217774444"})
    first_name=models.CharField(max_length=120, null=True,blank=True,default='')
    last_name=models.CharField(max_length=120, null=True,blank=True,default='')
    date_create=models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.subject} {self.email} "

class AboutusUs(models.Model):
    subject=models.CharField(max_length=5000, null=True,blank=True,default='')
    company=models.CharField(max_length=120, null=True,blank=True,default='')
    fburl=models.CharField(max_length=500, null=True,blank=True,default='')
    instaurl=models.CharField(max_length=500, null=True,blank=True,default='')
    logoimage=models.ImageField(upload_to='media/about',)

    email=models.EmailField(max_length=255, null=True,blank=True,default='')
    
    phone_number = PhoneNumberField(blank=True, unique=True,region="NZ",help_text="0064xxxxxxx format",error_messages={'invalid':"please reenter your number in 0064xxxxxxxxx format – e.g. 0064217774444"})
    address=models.CharField(max_length=5000, null=True,blank=True,default='')
    text1_heading=models.TextField(max_length=5000, null=True,blank=True,default='')
    text1_description=models.TextField(max_length=5000, null=True,blank=True,default='')
    text1_description2=models.TextField(max_length=5000, null=True,blank=True,default='')
    text1_images=models.ImageField(upload_to='media/about',)
    date_create=models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.text1_heading}" 