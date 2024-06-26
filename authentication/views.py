from django.contrib.auth.views import redirect_to_login

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView
from django.contrib.auth import logout
from django.urls import reverse_lazy
from glow.models import AboutusUs
from salonbooking.utils import Util
from .forms import UserCreationForm,OwnerUserCreationForm,OwnerUserChangeForm
from django.shortcuts import redirect, render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from .models import Region, UserProfile,SaloonTypes
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str, smart_bytes
from django.views.generic.edit import UpdateView ,FormView
@login_required
def logout_view(request):
    logout(request)
    return redirect('singin')
class signin(LoginView):
    template_name='authentication/login.html'
    next_page='index'
    redirect_authenticated_user=True
    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)   
        abs=AboutusUs.objects.first()                  
        context["about"] = abs
        return context


class signup(FormView):
    template_name = "authentication/singup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('verify-email')
    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)   
        abs=AboutusUs.objects.first()                  
        context["about"] = abs
        return context
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form.send_email()
        form.save(self.request)
       
        return super().form_valid(form)
    

   


    # return render(request, 'authentication/singup.html')
    
class owner(FormView):
    template_name = "authentication/singupassalonnonwe.html"
    form_class = OwnerUserCreationForm
    success_url = reverse_lazy('verify-email')
    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)   
        abs=AboutusUs.objects.first()                  
        context["about"] = abs
        return context
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save(self.request)
        
        return super().form_valid(form)
    
    
    
@login_required
def verify_email(request):
    if request.method == "POST":
        if request.user.email_is_verified != True:
            abs=AboutusUs.objects.first()
            current_site = get_current_site(request)
            user = request.user
            email = request.user.email
            subject = "Verify Email"
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = account_activation_token.make_token(user)
            
            message = render_to_string('authentication/emails/verify_email_message.html', {
                'request': request,
                'user': user,
                'domain': current_site.domain,
                'uid':uidb64,'about':abs,
                'token':token,
            })
            email = EmailMessage(
                subject, message, to=[email]
            )
            email.content_subtype = 'html'
            Util.send_email(email)
            return redirect('verify-email-done',)
        else:
            return redirect('index')
    if request.user.email_is_verified:
        return redirect('index')

    abs=AboutusUs.objects.first()
    
    return render(request, 'authentication/verify_email.html',{'about':abs})
@login_required
def verify_email_done(request):
    abs=AboutusUs.objects.first()
    if request.user.email_is_verified:
        return redirect('index')
    return render(request, 'authentication/verfiy_done.html',{'about':abs})


def verify_email_confirm(request, uidb64, token):
    abs=AboutusUs.objects.first()
    try:
        uid = smart_str(urlsafe_base64_decode(uidb64))

        user = UserProfile.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email_is_verified = True
        user.save()
        messages.success(request, 'Your email has been verified.')
        return redirect('verify-email-complete')   
    else:
        messages.warning(request, 'The link is invalid.')
    return render(request, 'authentication/verify_email_confirm.html',{'about':abs})

def verify_email_complete(request):
    abs=AboutusUs.objects.first()

    return render(request, 'authentication/verify_email_complete.html',{'about':abs})



class changepassword(SuccessMessageMixin,PasswordChangeView):
    template_name='authentication/changepassword.html'
    
    success_url=reverse_lazy("dashboard")
    success_message="You've successfully changed your password"

class forgortpassword(PasswordResetView):
    template_name='authentication/forgotpassword.html'
    html_email_template_name='authentication/emails/reset_pass_mail.html'
    email_template_name='authentication/emails/reset_pass_mail.html'
    def form_valid(self, form):
      opts = {
          'use_https': self.request.is_secure(),
          'token_generator': self.token_generator,
          'from_email': self.from_email,
          'email_template_name': self.email_template_name,
          'subject_template_name': self.subject_template_name,
          'request': self.request,
          'html_email_template_name': 'authentication/emails/reset_pass_mail.html',
          'extra_email_context': {'about': AboutusUs.objects.first()},
      }
      form.save(**opts)
      return HttpResponseRedirect(self.get_success_url())
    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)   
        abs=AboutusUs.objects.first()                  
        context["about"] = abs
        return context
    success_url=reverse_lazy("passwordrestdone")
class passwordRestDone(PasswordResetDoneView):
    template_name='authentication/passrestdone.html'
    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)   
        abs=AboutusUs.objects.first()                  
        context["about"] = abs
        return context
class passwordRestconfirm(SuccessMessageMixin,PasswordResetConfirmView):
    template_name='authentication/passrestconfirm.html'
    post_reset_login=False
    success_url=reverse_lazy("singin")
    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)   
        abs=AboutusUs.objects.first()                  
        context["about"] = abs
        return context
    success_message="You've successfully changed your password"

class userUpdateView(SuccessMessageMixin,UpdateView): 
    # specify the model you want to use 
    model = UserProfile
    # specify the fields 
    success_url=reverse_lazy("update")
    form_class = OwnerUserChangeForm
    # fields = ['address','company','first_name','last_name','phone_number','profile_image','webistelink','region']
    template_name='authentication/updateaccout.html'
    # can specify success url 
    # url to redirect after successfully 
    # updating details 
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), reverse_lazy('login'))
        if not request.user.email_is_verified:
            messages.warning(request,'Verify Your Email First')

            return HttpResponseRedirect(reverse_lazy('verify-email')) 
         # Redirect to email verification page
        return super().dispatch(request, *args, **kwargs)
    def get_object(self, queryset=None): 
        return self.request.user
    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = "Updated"
        rid = self.request.POST.get("regions")
        type = self.request.POST.get("saloontype")
        r = Region.objects.get(id=rid)
        if type!=None:
            ty = SaloonTypes.objects.get(id=type)
            self.request.user.type=ty
        self.request.user.region = r
        self.request.user.save()
        if success_message:
            messages.success(self.request, success_message)
        return response
    # def save(self,request,commit=False):
    #     # Sets username to email before saving
    #     user = super().save(commit=False)
    #     rid = self.cleaned_data.get('regions')
    #     r=Region.objects.get(id=rid)
    #     user.region=r 
    #     user.phone_number=self.cleaned_data.get('phone_number')
    #     user.webistelink=self.cleaned_data.get('webistelink')
    #     print(user)
    #     user.save()
       
    #     return user