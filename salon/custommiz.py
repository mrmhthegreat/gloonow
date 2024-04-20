from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from functools import wraps
from django.contrib import messages

from django.contrib.auth.views import redirect_to_login
def custom_user_passes_test_mixin(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        # Check if the user is logged in
        if not user.is_authenticated:
            return redirect_to_login(request.get_full_path(), reverse_lazy('login'))
        # Check if the user's email is verified
        elif not user.email_is_verified:
            messages.warning(request,'Verify Your Email First')
            return HttpResponseRedirect(reverse_lazy('verify-email'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view
class CustomUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        # Check if the user is logged in
        if not user.is_authenticated:
            return False
        # Check if the user's email is verified
        elif not user.email_is_verified:
            self.email_verification_required(self.request)
            return False
        return True


    def email_verification_required(self,request):
        # Redirect to email verification page
        messages.warning(request,'Verify Your Email First')
