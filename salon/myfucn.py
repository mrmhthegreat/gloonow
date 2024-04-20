from datetime import datetime
from django.utils.text import slugify

def timess(extra):
    dates=extra['dates']

    current_time = datetime.now().replace(second=0, microsecond=0)
    
    
    date={}
    for i in dates:
        if datetime.strptime(i.strip(), '%d %b %Y').replace(second=current_time.second, microsecond=current_time.microsecond,minute=current_time.minute,hour=current_time.hour)  >=current_time:
            date[i.strip()]=[]
    for i in date.keys():
        for key,value in extra[i].items():
            if  not value:
                if  datetime.strptime(i.strip()+" "+key.strip(), '%d %b %Y %I:%M %p').replace(second=0, microsecond=0)> current_time:
                    if date.get(i) is not None:
                        date[i.strip()].append(key)
                
    date['dates']=[]
    for i in date.keys():
        if(i!='dates'):
            if len(date[i])>0:
                date['dates'].append(i)
    date['datesa']=[]
    
    for i in date['dates']:
            choice_time = datetime.strptime(i.strip(), '%d %b %Y').replace(second=0, microsecond=0,minute=0,hour=0)
            ct=f"{choice_time.year}-{choice_time.month}-{choice_time.day}"
            date['datesa'].append(ct.strip())
    
    # if(current_time.day>choice_time_time)
    return date
def slugify_instance(instance,save=False,new_slug=None):
    if new_slug is not None:
        slug=new_slug
    else:
        slug=slugify(instance.slug)

    Klass=instance.__class__
    qs=Klass.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        slug=f"{slug}-{qs.count()+1}"
        return slugify_instance(instance,save=save,new_slug=slug)
    instance.slug=slug
    if save:
        instance.save()
    return instance

