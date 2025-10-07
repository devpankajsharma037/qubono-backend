from django.db import models
from customer.models import User
from core.utils.commonModel import CommonModel
from datetime import datetime
from django.utils.text import slugify
import string,random


class Category(CommonModel):
    name        = models.CharField(max_length=100)
    note        = models.TextField(blank=True,null=True)
    is_popular  = models.BooleanField(default=False)
    is_premium  = models.BooleanField(default=False)
    meta        = models.JSONField(blank=True,null=True)
    user        = models.ForeignKey(User,on_delete=models.CASCADE)
    slug        = models.SlugField(max_length=200,unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'Category'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or "store"
            slug = base_slug
            if Category.objects.filter(slug=slug).exists():
                random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
                slug = f"{base_slug}-{random_str}"
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.name} - {self.slug}'

class SubCategory(CommonModel):
    name        = models.CharField(max_length=100)
    note        = models.TextField(blank=True,null=True)
    is_popular  = models.BooleanField(default=False)
    is_premium  = models.BooleanField(default=False)
    meta        = models.JSONField(blank=True,null=True)
    user        = models.ForeignKey(User,on_delete=models.CASCADE)
    category    = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='sub_categorys')
    slug        = models.SlugField(max_length=200,unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'Sub Category'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or "store"
            slug = base_slug
            if SubCategory.objects.filter(slug=slug).exists():
                random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
                slug = f"{base_slug}-{random_str}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.slug}'
    
class Store(CommonModel):
    name        = models.CharField(max_length=100,blank=True,null=True)
    logo        = models.ImageField(upload_to="image/",blank=True,null=True)
    banner      = models.ImageField(upload_to="image/",blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    meta        = models.JSONField(blank=True,null=True)
    is_popular  = models.BooleanField(default=False)
    is_premium  = models.BooleanField(default=False)
    user        = models.ForeignKey(User,on_delete=models.CASCADE)
    website_url = models.URLField(max_length=800, blank=True, null=True)
    slug        = models.SlugField(max_length=200,unique=True, blank=True)
    category    = models.ManyToManyField(Category)
    sub_category    = models.ManyToManyField(SubCategory)
    contact_email   = models.EmailField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Store'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or "store"
            slug = base_slug
            if Store.objects.filter(slug=slug).exists():
                random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
                slug = f"{base_slug}-{random_str}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.slug}'

class DiscountType(models.TextChoices):
    FLAT        = "FLAT",
    PERCENTAGE   = "PERCENTAGE",

class CouponType(models.TextChoices):
    DEAL        = "DEAL", "DEAL"
    COUPON      = "COUPON", "COUPON"
    GIFT_CARD   = "GIFT_CARD", "GIFT_CARD"
    CASHBACK    = "CASHBACK", "CASHBACK"

class Coupon(CommonModel):
    name            = models.CharField(max_length=100)
    note            = models.TextField(blank=True,null=True)
    code            = models.CharField(max_length=100)
    validate_till   = models.DateTimeField()
    sub_category    = models.ManyToManyField(SubCategory)
    user            = models.ForeignKey(User,on_delete=models.CASCADE)
    stock           = models.IntegerField(default=1)
    is_popular      = models.BooleanField(default=False)
    discount        = models.CharField(max_length=50,blank=True,null=True)
    discount_type   = models.CharField(max_length=20,choices=DiscountType.choices,default='')
    is_premium      = models.BooleanField(default=False)
    available_stock = models.IntegerField(default=1)
    meta            = models.JSONField(blank=True,null=True)
    icon            = models.ImageField(upload_to="image/",blank=True,null=True)
    banner          = models.ImageField(upload_to="image/",blank=True,null=True)
    min_order_amount    = models.FloatField(blank=True,null=True)
    max_discount_amount = models.FloatField(blank=True,null=True)
    usage_limit     = models.IntegerField(default=1)
    usage_per_user  = models.IntegerField(default=1)
    term_conditions = models.TextField(blank=True,null=True)
    store           = models.ForeignKey(Store,on_delete=models.CASCADE,related_name="coupons")
    type            = models.CharField(max_length=20,choices=CouponType.choices,blank=True,default=CouponType.COUPON)

    class Meta:
        verbose_name_plural = 'Coupon'

class Wishlist(CommonModel):
    user    = models.ForeignKey(User,on_delete=models.CASCADE)
    store   = models.ForeignKey(Store,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Wishlist'

class NotificationType(models.TextChoices):
    COUPON_EXPIRY   = "COUPON_EXPIRY",
    NEW_DEAL        = "NEW_DEAL",
    PAYMENT         = "PAYMENT",

class Notification(CommonModel):
    user    = models.ForeignKey(User,on_delete=models.CASCADE)
    title   = models.CharField(max_length=100,blank=True,null=True)
    message = models.TextField(blank=True,null=True)
    type    = models.CharField(max_length=50,choices=NotificationType.choices,default=NotificationType.NEW_DEAL)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Notification'

class Rating(CommonModel):
    user        = models.ForeignKey(User,on_delete=models.CASCADE)
    store       = models.ForeignKey(Store,on_delete=models.CASCADE)
    title       = models.CharField(max_length=100,blank=True,null=True)
    message     = models.TextField(blank=True,null=True)
    is_approved = models.BooleanField(default=False)
    rating      = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = 'Rating'
