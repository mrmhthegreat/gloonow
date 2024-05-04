
# Create your views here.
from datetime import datetime
from django.shortcuts import  redirect, render,HttpResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import redirect_to_login

from django.views.generic import ListView
from django.views.generic.edit import FormView,FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from payment.models import Wallet
from salon.forms import BookingPostForm,FilterBook
from salon.models import BookingPost,BookBy, SaloonReview
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from salon.myfucn import timess
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import  Sum
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from authentication.models import UserProfile
from glow.models import ContactUs,AboutusUs,AppReview
from salon.custommiz import  custom_user_passes_test_mixin

def index(request):
    if request.user.is_authenticated:
        reviews=AppReview.objects.filter(Q(showin=True)|Q(user=request.user)).order_by('-bid')
    else:
        reviews=AppReview.objects.filter(Q(showin=True)).order_by('-bid')

    p=BookingPost.objects.search().order_by('-bookdatetime').order_by("-user__rating")[:10]
    form=FilterBook()
    ab=AboutusUs.objects.first()

    context={'products':p,'forms':form,'reviews':reviews,'about':ab}
    return render(request, 'booking/index.html',context)

def terms(request):
    ab=AboutusUs.objects.first()

    return render(request, 'terms.html',{'about':ab})
def Privacy(request):
    ab=AboutusUs.objects.first()

    return render(request, 'privacy.html',{'about':ab})
def contactus(request):
    abs=AboutusUs.objects.first()
    if request.method=="POST":
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        
        if  not subject or not email or not message:
            messages.warning(request,'Enter All Detail')
        else:
            if request.user.is_authenticated:

                c=ContactUs(subject=subject,message=message,email=email,
                            last_name=request.user.last_name,first_name=request.user.first_name,phone_number=request.user.phone_number
                            )
            else:
                c=ContactUs(subject=subject,message=message,email=email,
                           
                            )

            c.save()
            messages.success(request,'Message Send')

        return render(request, 'contactus.html',{'about':abs})


    return render(request, 'contactus.html',{'about':abs})


def about(request):
    abs=AboutusUs.objects.first()

    return render(request, 'about.html',{'about':abs})
@custom_user_passes_test_mixin
def dashboarrd(request):
    ab=AboutusUs.objects.first()
    
    return render(request, 'dashboard.html',{'about':ab})

class allreviews(ListView):

    model = SaloonReview
    template_name = "userbooking/allreviews.html"
    context_object_name = 'reviews'
    paginate_by=10
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), reverse_lazy('singin'))
        if not request.user.email_is_verified:
            messages.warning(request,'Verify Your Email First')

            return HttpResponseRedirect(reverse_lazy('verify-email')) 
         # Redirect to email verification page
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # self.publisher = get_object_or_404(BookingPost, user=self.request.user)
        if self.request.user.is_salonowner:
            return SaloonReview.objects.filter(saloon=self.request.user).order_by('-date_create').distinct()
        else:
            return SaloonReview.objects.filter(user=self.request.user).order_by('-date_create').distinct()


class mybookings(ListView):

    model = BookingPost
    template_name = "booking/owner/ownerallpost.html"
    context_object_name = 'bookings'
    paginate_by=10
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), reverse_lazy('singin'))
        if not request.user.email_is_verified:
            messages.warning(request,'Verify Your Email First')

            return HttpResponseRedirect(reverse_lazy('verify-email')) 
         # Redirect to email verification page
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        # self.publisher = get_object_or_404(BookingPost, user=self.request.user)
        return BookingPost.objects.filter(user=self.request.user,is_hide=False,is_book=False).order_by('-date_posted').distinct()
    def get_template_names(self):
        if self.request.user.is_salonowner:  # a certain check
            return [self.template_name]
        else:
            return ['404.html']
class mybooking(ListView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), reverse_lazy('singin'))
        if not request.user.email_is_verified:
            messages.warning(request,'Verify Your Email First')

            return HttpResponseRedirect(reverse_lazy('verify-email')) 
         # Redirect to email verification page
        return super().dispatch(request, *args, **kwargs)

    model = BookBy
    raise_exception=False
    template_name = "booking/owner/salonnallbooking.html"
    context_object_name = 'bookings'
    paginate_by=10
    def get_queryset(self):
        # self.publisher = get_object_or_404(BookingPost, user=self.request.user)
        if self.request.user.is_salonowner:
            return BookBy.objects.filter(saloon=self.request.user,payment=True,hideforowner=False).order_by('-date_create')
        else:
            return BookBy.objects.filter(user=self.request.user,payment=True,hideforuser=False).order_by('-date_create')

    
    def get_template_names(self):
        if self.request.user.is_salonowner:  # a certain check
            return ["booking/owner/salonnallbooking.html"]
        else:
            return ["userbooking/userallbooking.html"]


class createPost( SuccessMessageMixin,LoginRequiredMixin,FormView):
    template_name = "booking/owner/createpost.html"
    form_class = BookingPostForm
    success_url = reverse_lazy("ownerallpost")
    success_message="Post Create"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), reverse_lazy('singin'))
        if not request.user.email_is_verified:
            messages.warning(request,'Verify Your Email First')

            return HttpResponseRedirect(reverse_lazy('verify-email')) 
         # Redirect to email verification page
        return super().dispatch(request, *args, **kwargs)
    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs['request'] = self.request
        return form_kwargs
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save(self.request)
        return super().form_valid(form)
    def get_template_names(self):
        if self.request.user.is_salonowner:  # a certain check
            return [self.template_name]
        else:
            return ['404.html']
    

class PostListView( FormMixin,ListView):
    template_name = "booking/posts.html"
    context_object_name = "products"
    paginate_by = 10
    form_class = FilterBook
    # ordering = "user__rating"
    # new method added ⬇️
    def get_queryset(self):
      
        queryset=BookingPost.objects.search().order_by('bookdatetime').order_by("-user__rating")
        if self.request.POST.get("services")or self.request.POST.get("dates"):
            form = FilterBook(self.request.POST)
        

            if form.is_valid():
                selection =form.cleaned_data.get('services')
                date =form.cleaned_data.get('dates')
                if(date and selection ):
                    ct=datetime.strptime(date.strip(),'%d %b %Y')

                    queryset=BookingPost.objects.filterspecfice(ct,selection).order_by('-bookdatetime').order_by("-user__rating")
                elif(selection):
                    queryset = BookingPost.objects.filterspecficesv(selection).order_by('-bookdatetime').order_by("-user__rating")
                elif(date):
                    ct=datetime.strptime(date.strip(),'%d %b %Y')

                    queryset = BookingPost.objects.filterdatespecficesv(ct).order_by('-bookdatetime').order_by("-user__rating")
       
        return queryset
    
    def post(self, request, *args, **kwargs):
        
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        form=self.get_form()
        ab=AboutusUs.objects.first()

        if self.request.GET.get("services"):

            form = FilterBook(self.request.GET)
        context['forms'] = form # use from mixin instead manual init
        context['about'] = ab # use from mixin instead manual init
        return context

@login_required
def getimese(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == "POST":
            slug=request.POST.get('slug')
            dates=request.POST.get('dates')

            mo=BookingPost.objects.get(slug=slug)
            v=timess(mo.extra)
            choice_time = datetime.strptime(dates.strip(), '%Y-%m-%d').replace(second=0, microsecond=0,minute=0,hour=0)
            ct=choice_time.strftime('%d %b %Y')
            b= ct.strip()
            print(v[b])
            li=[]
            for i in v[b]:
                
                a=f'<li><input type="radio" id="{str(i)}" name="times" value="{str(i)}" class="hidden peer"> <label for="{str(i)}"   class="inline-flex items-center bg-slategray justify-between w-full p-3 text-gray-500  border border-gray-700 rounded-lg cursor-pointer bg-slategray  peer-checked:border-primary peer-checked:text-primary hover:text-white hover:bg-slategray"> <svg class="w-6 h-6 ms-3  mr-2  peer-checked:text-primary" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"  fill="none" viewBox="0 0 24 24">  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.5 11.5 11 14l4-4m6 2a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/></svg><div class="w-full  text-md  font-semibold">{i}</div></label></li> '
                li.append(a)
   
            return HttpResponse(li)
        else:
            return HttpResponseBadRequest('Invalid request')
    else:
        return HttpResponseBadRequest('Invalid request')
    
@custom_user_passes_test_mixin
def deactive(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == "POST":
            slug=request.POST.get('slug')
            tr=request.POST.get('tr')

            mo=BookingPost.objects.get(slug=slug,user=request.user)
            if tr=='0':
                mo.is_active=False
                mo.is_hide=True
            if tr=='1':
                mo.is_active=True

            mo.save()
            messages.success(request, f'{mo.title} Delete.')

            return HttpResponse('li')
        else:
            return HttpResponseBadRequest('Invalid request')
    else:
        return HttpResponseBadRequest('Invalid request')
    
@custom_user_passes_test_mixin
def canclebook(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == "POST":
            slug=request.POST.get('slug')
            type=request.POST.get('type')
            
            if type=='1':
                mo=BookBy.objects.get(id=slug,user=request.user)
                mo.hideforuser=True
                mo.save()
                messages.success(request, f'Delete.')
            else:

                mo=BookBy.objects.get(id=slug,user=request.user)
                bo=mo.booking
                bo.is_book=False
                bo.is_active=True
                bo.save()
                if(mo.payment):
                    mo.price;
                    w=Wallet.objects.get_or_create(user=mo.user,)
                    w[0].amount= w[0].amount+mo.price
                    w[0].save()

                mo.cancle=True
                mo.save()
                messages.success(request, f' Cancel.')

            return HttpResponse('li')
        else:
            return HttpResponseBadRequest('Invalid request')
    else:
        return HttpResponseBadRequest('Invalid request')
@custom_user_passes_test_mixin
def addreviesw(request):
    if request.method == "POST":
        rating=request.POST.get('rating')
        msg=request.POST.get('message')
        bid=request.POST.get('bid')
        id=request.POST.get('appreview')
        if not id and bid:
            bb=BookBy.objects.get(id=bid,user=request.user.id)
            if not bb.is_active:
                SU=UserProfile.objects.get(id=bb.saloon.id)
                sl=SaloonReview(rating=int(rating),
                            saloon=bb.saloon,
                            user=request.user,
                            
                            message=msg)
                t=SaloonReview.objects.filter(saloon=SU)
                if(t.count()>0):

                    tt=t.aggregate(
                        total=Sum('rating')
                    )["total"]
                
                    SU.rating=tt/t.count()
                else:
                    
                    SU.rating=5
                    
                SU.save()
                bb.is_active=True
                bb.save()
                sl.save()
            return redirect('allreviews')
        else:
            a,b=AppReview.objects.get_or_create(user=request.user)
           
            a.message=msg
            a.rating=int(rating)
            a.showin=False
            a.save()
            return redirect('index')
    else:
        return render("404.html")

def custom_404(request, exception):
    return render(request, '404.html', status=404)
