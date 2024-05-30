from django import forms

from salon.models import BookBy, BookingPost, TimeAdvance,AdvanceRequest,Services
from datetime import datetime
from django.db.models import Q
from glow.models import AboutusUs

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from salonbooking.utils import Util

from salon.myfucn import slugify_instance
class FilterBook(forms.Form):
    services = forms.ModelMultipleChoiceField(
        queryset=Services.objects.all(),
        widget=forms.CheckboxSelectMultiple,required=False)
    dates = forms.CharField(label="Dates", widget=forms.TextInput,required=False)
    def clean(self, *args, **kwargs):
        cleaned_data = super(FilterBook, self).clean(*args, **kwargs)
        services =cleaned_data.get('services')
        dates =cleaned_data.get('dates')
        return cleaned_data
    def filter_queryset(self, request, queryset):
        selection =self.form.cleaned_data.get('services')
        date =self.form.cleaned_data.get('dates')
        if(selection):
            if(date):
                choice_date = datetime.strptime(date.strip(), '%d %b %Y')

                lookup=Q(bookdate=choice_date)&Q(services__in=[x.id for x in selection])&Q(is_active=True)&Q(is_hide=False)&Q(is_book=False)
                
                return queryset.filter(lookup).order_by("user__rating")
            else:
                lookup=Q(services__in=[x.id for x in selection])&Q(is_active=True)&Q(is_hide=False)&Q(is_book=False)

                return  queryset.filter(lookup).order_by("user__rating")
        if(date):
            
            choice_date = datetime.strptime(date.strip(), '%d %b %Y')
            lookup=Q(bookdate=choice_date)&Q(is_active=True)&Q(is_hide=False)&Q(is_book=False)
            
            return queryset.filter(lookup).order_by("user__rating")
            
        return queryset


class BookingPostForm(forms.ModelForm):
    
    dates = forms.CharField(label="Dates", widget=forms.TextInput)
    times = forms.TimeField(label="Times")
    services = forms.ModelMultipleChoiceField(
        queryset=Services.objects.all(),
        widget=forms.CheckboxSelectMultiple)
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BookingPostForm, self).__init__(*args, **kwargs)
    class Meta:
        model = BookingPost
        fields = ['address','phone_number','title','message','services','dates','times',]
    
        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
    
    def clean(self, *args, **kwargs):
      
        cleaned_data = super(BookingPostForm, self).clean(*args, **kwargs)

        services =cleaned_data.get('services')
        dates =cleaned_data.get('dates')
        b=self.request.POST.get('times')
        
        if dates==None:
            self.add_error('dates', "Error Dates")
       
        if services ==None:
            self.add_error('services', "Select Services")
        elif len(services)<1:
            self.add_error('services', "Select Services")
        time_obj = datetime.strptime(b, '%H:%M')
        current_time = datetime.now().replace(second=0, microsecond=0)

        hour12=time_obj.strftime('%I:%M %p')

        choice_time = datetime.strptime(dates.strip()+" "+hour12.strip(), '%d %b %Y %I:%M %p').replace(second=0, microsecond=0)
        if choice_time < current_time:
            self.add_error('times', "Error Times")

        return cleaned_data
    def save(self,request,commit=False):
        # Sets username to email before saving
        post = super().save(commit=False)
        b=self.request.POST.get('times')
        dates =self.cleaned_data.get('dates')
        services =self.cleaned_data.get('services')
        title =self.cleaned_data.get('title')
        dates=dates.strip()


        time_obj = datetime.strptime(b, '%H:%M')

        hour12=time_obj.strftime('%I:%M %p')
        time_obj2 = datetime.strptime(hour12, '%I:%M %p')

        data={
            "dates":dates,'times':b,
            

        }
        datetimeobj = datetime.strptime(dates.strip()+" "+hour12.strip(), '%d %b %Y %I:%M %p').replace(second=0, microsecond=0)


        choice_date = datetime.strptime(dates.strip(), '%d %b %Y')
        
        
        
        post.extra=data
        post.bookdate=choice_date
        post.bookdatetime=datetimeobj
        post.booktime=time_obj2
        post.user=request.user
        post.t=request.user
        post.is_active=True
        post.title=title
        post.slug=f"{request.user.company} For {dates}-{hour12}"
        slugify_instance(post)

        post.save()
        # def filterspecfice(self,date,services,active=True):

        
        
        # qs=self.filter(lookup)
            
        # return qs.distinct()




        for sv in services:
            a=Services.objects.get(id=sv.pk)
            post.services.add(a)
        # for i in :
        
        # post.services=request.true

        lookup=Q(extra__dates__icontains=dates)&Q(services__in=[x.id for x in services])
        a=AdvanceRequest.objects.filter(lookup,times__starttime__lte=time_obj.time(),times__endtime__gte=time_obj.time()).distinct()
        issendto=[]
        k=[]
        for i in a:
            count=i.services.count()
            c=0
            for x in services:
                j=i.services.contains(x)
                if j:
                    c=c+1
            if count==c:
                if issendto.count(i.email)>0:
                    pass
                else:
                    issendto.append(i.email)
                    k.append(i)
            
        current_site = get_current_site(request)
                
        subject = "New Booking Available"
        
        abs=AboutusUs.objects.first()
        current_site = get_current_site(request)
        
        for i in k:
            message = render_to_string('booking/email/advancebook.html', {
            'request': request,
            'name': i.name,
            'user2': post.saloon,
            'urltopost': post.get_absolute_url(),
            'date':post.date,'about':abs,
            'domain': current_site.domain,
            'myser':','.join([x.name for x in i.services]),
            'time':post.time,
            'address':post.address,
            'services':',' .join([x.name for x in post.services.all()]),
            'salon':post.saloon.company,
            'domain': current_site.domain,
            'number':post.saloon.phone_number,
            'mail':post.saloon.email
        
            }) 

            email = EmailMessage(
                subject, message, to=[i.email.email]
            )

            email.content_subtype = 'html'
            Util.send_email(email)
            
        return post


class AdvancePostForm(forms.ModelForm):
    
    datesadv = forms.CharField(label="Dates", widget=forms.TextInput)
    # email = forms.EmailField(label="Email", widget=forms.TextInput)
    # name = forms.CharField(label="Name", widget=forms.TextInput)
    timesadv = forms.ModelMultipleChoiceField(queryset=TimeAdvance.objects.all(),widget=forms.CheckboxSelectMultiple)
    servicesadv = forms.ModelMultipleChoiceField(
        queryset=Services.objects.all(),
        widget=forms.CheckboxSelectMultiple)
    
        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
    class Meta:
        model = AdvanceRequest
        fields = ['servicesadv','timesadv','datesadv','name','email',]
    
    def clean(self, *args, **kwargs):
        cleaned_data = super(AdvancePostForm, self).clean(*args, **kwargs)
        services =cleaned_data.get('servicesadv')
        times =cleaned_data.get('timesadv')
        name =cleaned_data.get('name')
        dates =cleaned_data.get('datesadv')
        
        if dates==None:
            self.add_error('datesadv', "Error Dates")
        elif len(dates.split(','))<1:
            self.add_error('datesadv', "Select Dates")

        if services ==None:
            self.add_error('servicesadv', "Select Services")

        elif len(services)<1:
            self.add_error('servicesadv', "Select Service")
        if times==None:
            self.add_error('timesadv', "Select Times")
        elif len(times)<1:
            self.add_error('timesadv', "Select Times")
        if name==None:
            self.add_error('name', "Enter Valid Name")  
        elif len(name)<1:
            self.add_error('name', "Enter Valid Name")
        
        
        return cleaned_data
    def save(self,request,commit=False):
        # Sets username to email before saving
        post = super().save(commit=False)
        dates =self.cleaned_data.get('datesadv').split(',')
        services =self.cleaned_data.get('servicesadv')
        times =self.cleaned_data.get('timesadv')
        email =self.cleaned_data.get('email')
        name =self.cleaned_data.get('name')
        dates=[x.strip() for x in dates]
        data={
            "dates":dates,
            

        }
        
        post.extra=data
        post.email=email
        post.name=name
        post.slug=f"{name}  {email } From {dates[0]} To {dates[-1]}"
        slugify_instance(post)
        post.save()
        for sv in services:
            a=Services.objects.get(id=sv.pk)
            post.services.add(a)
        for sv in times:
            a=TimeAdvance.objects.get(id=sv.pk)
            post.times.add(a)
        
        


            
        return post
