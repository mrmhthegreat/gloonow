from django.db import models

# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin)
# from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.
# from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .usermanager import CustomUserManager
AUTH_PROVIDERS = {'google': 'google',
                  'email': 'email'}

class SaloonTypes(models.Model):
    name = models.CharField(max_length=1000)
    image = models.ImageField(blank=True,upload_to='profile',null=True,default='profile/capture.png')
    perority = models.IntegerField( default=0,null=False,blank=False)
    class Meta:
        ordering = ['-perority']
    def __str__(self):
        return self.name
class Region(models.Model):
    name = models.CharField(max_length=700)
    def __str__(self):
        return self.name
class UserProfile(AbstractBaseUser,PermissionsMixin):
    username = None
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    email_is_verified = models.BooleanField(default=False)
    profile_image = models.ImageField(blank=True,upload_to='profile',null=True,default='profile/capture.png')
    address = models.CharField(max_length=120,null=True,blank=True, default='')
    company = models.CharField(max_length=120, null=True,blank=True,default='')
    rating = models.DecimalField(max_digits=2,default=0, null=True,blank=True,decimal_places=1)
    extra = models.JSONField(null=True)
    type=models.ForeignKey(SaloonTypes,null=True,blank=True,on_delete=models.CASCADE)
    phone_number = PhoneNumberField(blank=True, unique=True,help_text="0064xxxxxxx format",error_messages={'invalid':"please reenter your number in 0064xxxxxxxxx format – e.g. 0064217774444"})
    first_name=models.CharField(max_length=120, null=False,blank=False,default='')
    last_name=models.CharField(max_length=120, null=True,blank=True,default='')
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_salonowner = models.BooleanField(default=False)
    is_staff = models.BooleanField(_('staff status'), default=False,help_text=_('Designates whether the user can log into this admin ''site.'))
    is_active = models.BooleanField(_('active'), default=True,help_text=_('Designates whether this user should be treated as ''active. Unselect this instead of deleting accounts.'))
    is_admin=models.BooleanField(default=False)
    token=models.CharField(default='token will  genrated in feature',max_length=500)
    region=models.ForeignKey(Region,null=True,blank=True,on_delete=models.CASCADE)
    webistelink=models.CharField(null=True,blank=True,max_length=500)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    def get_full_name(self):
        return self.first_name +" "+ self.last_name
    def get_short_name(self):
        return self.last_name
   # def has_perm(self,perm,obj):
       
    #    if self.is_active and self.is_superuser:
     #       return True
        # return this.groups.values_list(self.email,flat=True)
      #  return _user_has_perm(self,perm.obj)
    def __unicode__(self):
        return self.email
    def get_group(self):
        return self.objects.values('groups')
    def __str__(self):
        return self.email
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    def save(self, *args, **kwargs):
        if self.webistelink !=None:

            self.webistelink=self.webistelink if self.webistelink.startswith("https://") else f"https://{self.webistelink}"

        super().save(*args, **kwargs)
