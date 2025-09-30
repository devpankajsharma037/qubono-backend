from django.db import models
from customer.models import User
from core.utils.commonModel import CommonModel
from datetime import datetime
from coupon.models import Coupon
import string, random
from django.utils.timezone import now

def generateOrderId():
    date_str    = now().strftime("%Y%m%d")
    random_str  = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    unique_num  = str(int(datetime.timestamp(now())))[-5:]
    return f"{date_str}{random_str}{unique_num}"

class PaymentType(models.TextChoices):
    PROCESS   = "PROCESS",
    SUCCESS   = "SUCCESS",
    FAILED    = "FAILED",
    PENDING   = "PENDING",
    CANCELLED = "CANCELLED",
    REFUNDED  = "REFUNDED",

class Payment(CommonModel):
    price           = models.FloatField()
    platform_name   = models.CharField(max_length=50)
    status          = models.CharField(max_length=20,choices=PaymentType.choices,default=PaymentType.PENDING)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id      = models.CharField(max_length=50,null=True,blank=True)
    invoice_id      = models.CharField(max_length=150,null=True,blank=True)
    meta            = models.JSONField(null=True,blank=True)
    transaction_date= models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name_plural = 'Payment'

class Order(CommonModel):
    coupon          = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    payment         = models.ForeignKey(Payment, on_delete=models.CASCADE)
    order_id        = models.CharField(max_length=50)
    total_amount    = models.FloatField(max_length=50,null=True,blank=True)
    discount_amount = models.FloatField(max_length=50,null=True,blank=True)
    final_amount    = models.FloatField(max_length=50,null=True,blank=True)
    order_date      = models.DateTimeField(default=datetime.now)
    delivery_address    = models.TextField(null=True,blank=True)
    meta                = models.JSONField(null=True,blank=True)
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = generateOrderId()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Order'

class CouponUsage(CommonModel):
    coupon              = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    order               = models.ForeignKey(Order, on_delete=models.CASCADE)
    used_at             = models.DateTimeField(default=datetime.now)
    discount_applied    = models.FloatField(max_length=50,null=True,blank=True)
    meta                = models.JSONField(null=True,blank=True)

    class Meta:
        verbose_name_plural = 'Coupon Usage'