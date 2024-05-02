from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.utils.text import slugify
from payment.models import Wallet
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

from django.utils.decorators import method_decorator
from glow.models import AboutusUs
from salon.models import BookBy, BookingPost, Services,UserProfile
from django.contrib import messages
from salon.myfucn import timess,slugify_instance
from salon.custommiz import custom_user_passes_test_mixin
from .models import Price,Payment
# Create your views here.
from django.views.decorators.csrf import csrf_exempt # new
from django.conf import settings
import stripe
from datetime import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from salonbooking.utils import Util
from django.views.generic import TemplateView

from django.http import HttpResponse, HttpResponseBadRequest
@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):
    """
    Stripe webhook view to handle checkout session completed event.
    """

    def post(self, request, format=None):
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
            
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        if event["type"] == "checkout.session.completed":
            print("Payment successful")
            data=event["data"]["object"]
            session = data["metadata"]["product_id"]

            id = data["metadata"]["userid"]
            bb=BookBy.objects.get(id=session)
            bbk=BookingPost.objects.get(id=bb.booking.id)
            

            up=UserProfile.objects.get(id=id )
            bb.payment=True
            bb.payment_id=data['id']
            
            bbk.is_book=True
            bbk.is_active=False

            bbk.save()
            bb.save()
            pp=Payment.objects.create(book_id=bb,payment_id=data['id'],user=up,is_done=True,payment_status="C",price=float(data['amount_total']/100))
            pp.save()
           
         
            current_site = get_current_site(request)
            
            subject = "Appointment Booking Receipt"
            subject2 = "Appointment Request"
            abs=AboutusUs.objects.first()
            current_site = get_current_site(request)

            messages.success(request,"Booked")
            message = render_to_string('booking/email/bookinforuseremail.html', {
                'request': request,
                'user': bb.user,
                'user2': bb.saloon,
                'domain': current_site.domain,
                'date':bb.date,
                'time':bb.time,'about':abs,
                'address':bb.address,
                'services':[x.name for x in bb.services.all()],
                'salon':bb.saloon.company,
                'domain': current_site.domain,
                'number':bb.saloon.phone_number,
                'mail':bb.saloon.email
             
            }) 
            message2 = render_to_string('booking/email/bookingforsalonemail.html', {
                'request': request,
                'user': bb.user,
                'user2': bb.saloon,
                'domain': current_site.domain,
                'date':bb.date,
                'time':bb.time,'about':abs,
                'address':bb.address,
                'services':[x.name for x in bb.services.all()],
                'salon':bb.saloon.company,
                'domain': current_site.domain,
                'number':bb.saloon.phone_number,
                'mail':bb.saloon.email
             
            })
            email = EmailMessage(
                subject, message, to=[bb.user.email]
            )
            email2 = EmailMessage(
                subject2, message2, to=[bb.saloon.email]
            )
            
            email.content_subtype = 'html'
            email2.content_subtype = 'html'
            Util.send_email(email)
            Util.send_email(email2)
            
            # session = data["object"]
            # customer_email = session["customer_details"]["email"]
            # product_id = session["metadata"]["product_id"]
        # Can handle other events here.
        
        else:
            print(event["type"])
            print(event["data"])

        return HttpResponse(status=200)
class bookings(View,LoginRequiredMixin):
    def post(self, request,slug):
        # handle the post request
        mo=BookingPost.objects.get(slug=slug)
        service=request.POST.getlist('services')
        
        if  request.user.is_salonowner or not self.request.user.is_authenticated:
            messages.warning(request,'You Can not Book Register As Normal User')
            v=timess(mo.extra)
            context={'post':mo,'times':v}
            return render(request, 'payment/booknow.html',context)


        times=mo.booktime.strftime('%I:%M %p')
        dates=mo.bookdate.strftime('%d %b %Y')

      
        has=mo.is_book
        
      
        if( len(service)<1 or  has):
            messages.warning(request,'Pick Date, Time and Serivecs')
            v=timess(mo.extra)
            context={'post':mo,'times':v}
            return render(request, 'payment/booknow.html',context)
       
        else:
            
            extra={'first_name':request.POST.get('first_name'),'last_name':request.POST.get('last_name')}
            bookby=BookBy(slug=slugify(f"Book by {request.user.email} At {dates} {times} With {mo.user.company}"),
                   user=request.user,
                   saloon=mo.user,
                   booking=mo,
                   message=request.POST.get('message'),
                   time=times,
                   date=dates,
                   phone_number=request.POST.get('phone'),
                   address=mo.user.address,
                   extra=extra
                   )
            slugify_instance(bookby)
            
            bookby.save()
            for sv in service:
                a=Services.objects.get(id=sv)
                bookby.services.add(a)
            
            stripe.api_key = settings.STRIPE_SECRET_KEY

            price = Price.objects.first()
            wallet=Wallet.objects.get_or_create(user=request.user)
            if(wallet[0].amount>=price.price):

                bbk=BookingPost.objects.get(id=bookby.booking.id)
            

                up=UserProfile.objects.get(id=request.user.id )
                bookby.payment=True
                bookby.payment_id="Walelt"
                
                bbk.is_book=True
                bbk.is_active=False


                bbk.save()
                bookby.save()
                pp=Payment.objects.create(book_id=bookby,payment_id='Wallet',user=up,is_done=True,payment_status="C",price=price.price)
                pp.save()
           
         
                current_site = get_current_site(request)
                
                subject = "Appointment Booking Receipt"
                subject2 = "Appointment Request"
                wallet[0].amount=wallet[0].amount-price.price
                wallet[0].save()
                messages.success(request,"Booked")
                abs=AboutusUs.objects.first()
                current_site = get_current_site(request)

                message = render_to_string('booking/email/bookinforuseremail.html', {
                    'request': request,
                    'user': bookby.user,
                    'user2': bookby.saloon,
                    'date':bookby.date,'about':abs,
                    'domain': current_site.domain,
                    'time':bookby.time,
                    'address':bookby.address,
                    'services':[x.name for x in bookby.services.all()],
                    'salon':bookby.saloon.company,
                    'domain': current_site.domain,
                    'number':bookby.saloon.phone_number,
                    'mail':bookby.saloon.email
                
                }) 
                message2 = render_to_string('booking/email/bookingforsalonemail.html', {
                    'request': request,
                    'user': bookby.user,
                    'user2': bookby.saloon,'about':abs,
                    'date':bookby.date,
                    'domain': current_site.domain,
                    'time':bookby.time,
                    'address':bookby.address,
                    'services':[x.name for x in bookby.services.all()],
                    'salon':bookby.saloon.company,
                    'domain': current_site.domain,
                    'number':bookby.saloon.phone_number,
                    'mail':bookby.saloon.email
                
                })
                email = EmailMessage(
                    subject, message, to=[bookby.user.email]
                )
                email2 = EmailMessage(
                    subject2, message2, to=[bookby.saloon.email]
                )
                
                email.content_subtype = 'html'
                email2.content_subtype = 'html'
                Util.send_email(email)
                Util.send_email(email2)
                return redirect('success')
            checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(price.price) * 100,
                        "product_data": {
                            "name": "Glow Booking",
                            "description": f"{bookby.user.first_name} Book {bookby.saloon.company} {bookby.date} {bookby.time} For {[x.name for x in bookby.services.all()]}",
                            "images": [
                                f"{settings.BACKEND_DOMAIN}/{bookby.saloon.profile_image.url}"
                            ],
                        },
                    },
                    "quantity": 1,
                }
            ],
            metadata={"product_id": bookby.id,"slug":bookby.slug,"userid":bookby.user.id},
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )
            
        
        return redirect(checkout_session.url)
            
        
        

    def get(self, request,slug):
        # handle the get request
        mo=BookingPost.objects.get(slug=slug)
        context={'post':mo,}
        current_time = datetime.now().replace(second=0, microsecond=0)
        
        if(mo.is_book):
            return redirect("index")
        return render(request, 'payment/booknow.html',context)
    

def refund(request):
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        payment_id = request.POST['payment_id']
        try:
            refund = stripe.Refund.create(
                charge=payment_id
            )
            
            # Process successful refund
            return render(request, 'refund_success.html')
        
        except stripe.error.StripeError as e:
            # Handle refund error
            return render(request, 'refund_error.html', {'error': e})
        
        except Exception as e:
            # Handle other exceptions
            return render(request, 'refund_error.html', {'error': e})
    return render(request, 'refund.html')

@custom_user_passes_test_mixin
def approveOrreject(request):
    print(request)
    
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == "POST":
            slug=request.POST.get('slug')
            tr=request.POST.get('tr')
            print(slug)
            current_site = get_current_site(request)

            bk=BookBy.objects.get(id=slug,saloon=request.user)
            abs=AboutusUs.objects.first()
            if tr=='3':
                bk.hideforowner=True
                messages.success(request, f'Delete.')
            if tr=='0':
                bk.confirm=False
                bk.reject=True
                w=Wallet.objects.get_or_create(user=bk.user,)
                w[0].amount= w[0].amount+bk.price
                w[0].save()
                subject = "Appointment Rejected"
                bookin=bk.booking
                bookin.is_book=False
                bookin.is_active=True
                current_site = get_current_site(request)

                bookin.save()
                message = render_to_string('booking/email/bookingreject.html', {
                    'request': request,
                    'user': bk.user,
                    'user2': bk.saloon,'about':abs,
                    'domain': current_site.domain,
                    'date':bk.date,
                    'time':bk.time,
                    'address':bk.address,
                    'services':[x.name for x in bk.services.all()],
                    'salon':bk.saloon.company,
                    'domain': current_site.domain,
                    'number':bk.saloon.phone_number,
                    'mail':bk.saloon.email
                
                }) 
             
                email = EmailMessage(
                    subject, message, to=[bk.user.email]
                )
               
                email.content_subtype = 'html'
                Util.send_email(email)
                messages.success(request, 'Appointment Rejected.')

            if tr=='1':
                current_site = get_current_site(request)
                
                subject = "Appointment Confirmed"
                bk.confirm=True
                message = render_to_string('booking/email/bookingconfirm.html', {
                    'domain': current_site.domain,
                    'request': request,
                    'user': bk.user,
                    'user2': bk.saloon,
                    'date':bk.date,
                    'time':bk.time,'about':abs,
                    'address':bk.address,
                    'services':[x.name for x in bk.services.all()],
                    'salon':bk.saloon.company,
                    'domain': current_site.domain,
                    'number':bk.saloon.phone_number,
                    'mail':bk.saloon.email
                
                }) 
             
                email = EmailMessage(
                    subject, message, to=[bk.user.email]
                )
               
                email.content_subtype = 'html'
                Util.send_email(email)
                messages.warning(request, 'Appointment Confirmed.')

            bk.save()

            return HttpResponse('li')
        else:
            return HttpResponseBadRequest('Invalid request')
    else:
        return HttpResponseBadRequest('Invalid request')
    
class SuccessView(TemplateView):
    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)   
        abs=AboutusUs.objects.first()                  
        context["about"] = abs
        return context
    template_name = "payment/success.html"

class CancelView(TemplateView):
    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)   
        abs=AboutusUs.objects.first()                  
        context["about"] = abs
        return context
    template_name = "payment/cancel.html"