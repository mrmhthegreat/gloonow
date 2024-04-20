from django import forms

from salon.models import BookBy, BookingPost, Services
from datetime import datetime

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
                        
                return queryset.filter(extra__dates__icontains=date,services__in=[x.id for x in selection]).exclude(is_active=False).order_by("user__rating")
            else:
                return  queryset.filter(services__in=[x.id for x in selection])
        if(date):
            
                        
            return queryset.filter(extra__dates__icontains=date,).exclude(is_active=False).order_by("user__rating")
            
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
    times = forms.MultipleChoiceField(choices=CHOICES,widget=forms.CheckboxSelectMultiple)
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
        b=self.request.POST.getlist('times')
        if dates==None:
            self.add_error('dates', "Error Dates")
        elif len(dates.split(','))<1:
            self.add_error('dates', "Select Dates")

        if services ==None:
            self.add_error('services', "Select Services")

        elif len(services)<1:
            self.add_error('services', "Select Service")
        elif len(b)<1:
            self.add_error('time', "Select Times")

     
        return cleaned_data
    def save(self,request,commit=False):
        # Sets username to email before saving
        post = super().save(commit=False)
        b=self.request.POST.getlist('times')
        dates =self.cleaned_data.get('dates').split(',')
        services =self.cleaned_data.get('services')
        title =self.cleaned_data.get('title')
        dates=[x.strip() for x in dates]
        b=[x.strip() for x in b]
        data={
            "dates":dates,'times':b,
            

        }
        b.sort()
        dates.sort()
        current_time = datetime.now().replace(second=0, microsecond=0)

        
        for tim in dates:
            data[tim.strip()]={}
        for tim in dates:
           
            for time in b:
                choice_time = datetime.strptime(tim.strip()+" "+time.strip(), '%d %b %Y %I:%M %p').replace(second=0, microsecond=0)
                print(choice_time)
                if choice_time > current_time:
                    if data.get(tim) is not None:
                        data[tim.strip()][time.strip()]=False
        post.extra=data
        post.user=request.user
        post.is_active=True
        post.title=title
        post.slug=f"{request.user.company} From {dates[0]} To {dates[-1]}"
        slugify_instance(post)

        post.save()
        for sv in services:
            a=Services.objects.get(id=sv.pk)
            post.services.add(a)
        # for i in :
        
        # post.services=request.true


            
        return post


