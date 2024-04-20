from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import UserProfile
from django.contrib.auth import authenticate, login

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    phone_number = PhoneNumberField(region="PK")
    class Meta:
        model = UserProfile
        fields = ["email",'first_name','last_name','phone_number','profile_image','password']

 
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        email_check = UserProfile.objects.filter(email=email)
        if email_check.exists():
            self.add_error('email', 'This Email already exists')
        if len(password) < 5:
            self.add_error('email','Your password should have more than 5 characters')
        return super(UserCreationForm, self).clean(*args, **kwargs)
    def save(self,request,commit=False):
        # Sets username to email before saving
        user = super().save(commit=False)
        print(user)

        password = self.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(email=user.email, password=password)
        login(request, new_user)
            
        return user


class OwnerUserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    phone_number = PhoneNumberField(region="PK")
    

    class Meta:
        model = UserProfile
        fields = ["email",'address','company','first_name','last_name','phone_number','profile_image','password']

 
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        email_check = UserProfile.objects.filter(email=email)
        if email_check.exists():
            self.add_error('email', 'This Email already exists')
        if len(password) < 5:
            self.add_error('email','Your password should have more than 5 characters')
        return super(OwnerUserCreationForm, self).clean(*args, **kwargs)
   
    def save(self,request,commit=False):
        # Sets username to email before saving
        user = super().save(commit=False)
        print(user)

        password = self.cleaned_data.get('password')
        user.set_password(password)
        user.is_salonowner=True 

        user.save()
        new_user = authenticate(email=user.email, password=password)
        login(request, new_user)
            
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()
    phone_number = PhoneNumberField(region="CA")
    class Meta:
        model = UserProfile
        fields = ["email",'password', "email_is_verified",'address','company','is_active','is_salonowner','first_name','last_name','phone_number','profile_image']

