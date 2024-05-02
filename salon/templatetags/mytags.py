from django import template
from datetime import datetime
from django.utils.safestring import mark_safe
from django.contrib.humanize.templatetags.humanize import ordinal
import json


register = template.Library()

@register.filter
def lower(value):
    return value.lower()
@register.filter()
def bold_time(dates):
    current_time = datetime.now().replace(second=0, microsecond=0,minute=0,hour=0)
    ct=current_time.strftime('%d %b %Y')
    date=[]
    for i in dates:
        if i.strip() >=ct:
            date.append(i)

   
    # choice_time = datetime.strptime(time.strip()+" "+time.strip(), '%d %b %Y %I:%M %p').replace(second=0, microsecond=0,minute=0,hour=0)
    # if(current_time.day>choice_time_time)
    return date
@register.filter()
def hourampm(times):
    return times.strftime('%I:%M %p')
@register.filter(s_safe=True)
def dayyear(dates):
        # text += ('<p class="site-description">' + i + '</p>')
    # return mark_safe(text)
    # Get the day name, month name, and month day
    day_name = dates.strftime('%a %b')  # Full weekday name
    month_day = dates.strftime('%d')  # Day of the month
    

    suffix = 'th' if 11 <= int(month_day) <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(int(month_day) % 10, 'th')


    formatted_date = f"{day_name} {int(month_day)}<sup>{suffix}</sup>  "
    
    return mark_safe(formatted_date)

@register.filter()
def times(extra):
    dates=extra['dates']
    time=extra['times']

    current_time = datetime.now().replace(second=0, microsecond=0)
    ct=current_time.strftime('%d %b %Y')
    ct2=current_time.strftime('%I:%M %p')
    
    date={}
    for i in dates:
        if datetime.strptime(i.strip(), '%d %b %Y').replace(second=current_time.second, microsecond=current_time.microsecond,minute=current_time.minute,hour=current_time.hour)  >=current_time:
            date[i.strip()]=[]
    for i in date.keys():
        for key,value in extra[i].items():
            if  not value:
                if  datetime.strptime(i.strip()+" "+key.strip(), '%d %b %Y %I:%M %p').replace(second=0, microsecond=0)> current_time:
                    if date.get(i) is not None:
                        date[i.strip()].append(key.strip())
                

   
    # choice_time = datetime.strptime(time.strip()+" "+time.strip(), '%d %b %Y %I:%M %p').replace(second=0, microsecond=0,minute=0,hour=0)
    # if(current_time.day>choice_time_time)
    return date.items()


@register.filter()
def booktimes(extra):
    dates=extra['dates']
    
    
    
    date={}
    for i in extra.keys():
        if i=="dates" or i=="times":
            pass
        else:
            for key,value in extra[i].items():
                if  value:
                    
                    if date.get(i) is not None:
                        date[i.strip()].append(key.strip())
                    else:
                        date[i.strip()]=[key.strip()]

                

   
    # choice_time = datetime.strptime(time.strip()+" "+time.strip(), '%d %b %Y %I:%M %p').replace(second=0, microsecond=0,minute=0,hour=0)
    # if(current_time.day>choice_time_time)
    return date.items()

@register.filter()
def poptimes(extra):
    dates=extra['dates']
    
    
    
    date={}
    leng=0
    for i in dates:
        for key,value in extra[i].items():
            if  value:
                
                if date.get(i) is not None:
                    leng=leng+1
                    date[i.strip()].append(key.strip())
                else:
                    leng=leng+1

                    date[i.strip()]=[key.strip()]

                

   
    # choice_time = datetime.strptime(time.strip()+" "+time.strip(), '%d %b %Y %I:%M %p').replace(second=0, microsecond=0,minute=0,hour=0)
    # if(current_time.day>choice_time_time)
    return leng

@register.filter()
def timeslist(extra):
    return extra.getlist('services')
@register.filter()
def dictvalue(extra,key):
    return extra[key]
@register.filter()
def dictlist(extra):
    choice_time = datetime.strptime(extra.strip(), '%Y-%m-%d').replace(second=0, microsecond=0,minute=0,hour=0)
    ct=choice_time.strftime('%d %b %Y')
    return ct.strip()
@register.filter()
def tostr(extra):
    return str(extra)



@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))

@register.filter()
def isafter(time,date):

    current_time = datetime.now().replace(second=0, microsecond=0)
   
    
    if datetime.strptime(date.strip()+" "+time.strip(), '%d %b %Y %I:%M %p').replace(second=0, microsecond=0) < current_time:
        return True
    else: 
        False
                   
                


