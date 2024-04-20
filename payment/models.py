from django.db import models
from django.utils.translation import gettext_lazy as _

from salon.models import BookBy,UserProfile

# Create your models here.
class Price(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=10)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.price}"
class Payment(models.Model):
    
    PENDING = "P"
    COMPLETED = "C"
    FAILED = "F"

    STATUS_CHOICES = (
        (PENDING, _("pending")),
        (COMPLETED, _("completed")),
        (FAILED, _("failed")),
    )
    payment_status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=PENDING
    )
    price = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="payment_user")
    book_id = models.OneToOneField(BookBy,on_delete=models.CASCADE,related_name="book_id")
    payment_id=models.CharField(max_length=5000, null=True,blank=True,default='')
    is_done=models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.price}"
class Wallet(models.Model):
    
 
    
    amount = models.DecimalField(decimal_places=2, max_digits=10,default=0.0)
    user = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return f"{self.user.first_name} has {self.amount} in Wallet"