from django import forms

from salon.models import BookBy, BookingPost, Services
from datetime import datetime
from django.db.models import Q

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
    
    CHOICES = [
        ('12:00 AM', '12:00 AM'),
        ('12:30 AM', '12:30 AM'),
        ('01:00 AM', '01:00 AM'),
        ('01:30 AM', '01:30 AM'),
        ('02:00 AM', '02:00 AM'),
        ('02:30 AM', '02:30 AM'),
        ('03:00 AM', '03:00 AM'),
        ('03:30 AM', '03:30 AM'),
        ('04:00 AM', '04:00 AM'),
        ('04:30 AM', '04:30 AM'),
        ('05:00 AM', '05:00 AM'),
        ('05:30 AM', '05:30 AM'),
        ('06:00 AM', '06:00 AM'),
        ('06:30 AM', '06:30 AM'),
        ('07:00 AM', '07:00 AM'),
        ('07:30 AM', '07:30 AM'),
        ('08:00 AM', '08:00 AM'),
        ('08:30 AM', '08:30 AM'),
        ('09:00 AM', '09:00 AM'),
        ('09:30 AM', '09:30 AM'),
        ('10:00 AM', '10:00 AM'),
        ('10:30 AM', '10:30 AM'),
        ('11:00 AM', '11:00 AM'),
        ('11:30 AM', '11:30 AM'),
        ('12:00 PM', '12:00 PM'),
        ('12:30 PM', '12:30 PM'),
        ('01:00 PM', '01:00 PM'),
        ('01:30 PM', '01:30 PM'),
        ('02:00 PM', '02:00 PM'),
        ('02:30 PM', '02:30 PM'),
        ('03:00 PM', '03:00 PM'),
        ('03:30 PM', '03:30 PM'),
        ('04:00 PM', '04:00 PM'),
        ('04:30 PM', '04:30 PM'),
        ('05:00 PM', '05:00 PM'),
        ('05:30 PM', '05:30 PM'),
        ('06:00 PM', '06:00 PM'),
        ('06:30 PM', '06:30 PM'),
        ('07:00 PM', '07:00 PM'),
        ('07:30 PM', '07:30 PM'),
        ('08:00 PM', '08:00 PM'),
        ('08:30 PM', '08:30 PM'),
        ('09:00 PM', '09:00 PM'),
        ('09:30 PM', '09:30 PM'),
        ('10:00 PM', '10:00 PM'),
        ('10:30 PM', '10:30 PM'),
        ('11:00 PM', '11:00 PM'),
        ('11:30 PM', '11:30 PM')
    ]
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
        
        a=Services.objects.get(id=services)
        post.services.add(a)
        # for i in :
        
        # post.services=request.true


            
        return post


