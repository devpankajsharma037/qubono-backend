from django.db import models
from customer.models import User
from core.utils.commonModel import CommonModel
from datetime import datetime,timezone

class Merchant(CommonModel):
    name        = models.CharField(max_length=100,blank=True,null=True)
    logo        = models.ImageField(upload_to="image/",blank=True,null=True)
    banner      = models.ImageField(upload_to="image/",blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    meta        = models.JSONField(blank=True,null=True)
    is_popular  = models.BooleanField(default=False)
    is_premium  = models.BooleanField(default=False)
    user        = models.ForeignKey(User,on_delete=models.CASCADE)
    website_url = models.URLField(max_length=800, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Merchant'

class Deal(CommonModel):
    name            = models.CharField(max_length=100)
    icon            = models.ImageField(upload_to="image/",blank=True,null=True)
    banner          = models.ImageField(upload_to="image/",blank=True,null=True)
    slug            = models.URLField(max_length=800, blank=True, null=True)
    meta            = models.JSONField(blank=True,null=True)
    note            = models.TextField(blank=True,null=True)
    is_popular      = models.BooleanField(default=False)
    is_premium      = models.BooleanField(default=False)
    user            = models.ForeignKey(User,on_delete=models.CASCADE)
    merchant        = models.ForeignKey(Merchant,on_delete=models.CASCADE)
    orignal_price   = models.FloatField()
    discount_price  = models.FloatField(blank=True,null=True)
    valid_from      = models.DateTimeField(default=datetime.now)
    valid_until     = models.DateTimeField()
    term_conditions = models.TextField(blank=True,null=True)

    class Meta:
        verbose_name_plural = 'Deal'

class Category(CommonModel):
    name        = models.CharField(max_length=100)
    note        = models.TextField(blank=True,null=True)
    is_popular  = models.BooleanField(default=False)
    is_premium  = models.BooleanField(default=False)
    meta        = models.JSONField(blank=True,null=True)
    merchant    = models.ForeignKey(Merchant,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Category'

class SubCategory(CommonModel):
    name        = models.CharField(max_length=100)
    note        = models.TextField(blank=True,null=True)
    is_popular  = models.BooleanField(default=False)
    is_premium  = models.BooleanField(default=False)
    meta        = models.JSONField(blank=True,null=True)
    category    = models.ForeignKey(Category,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Sub Category'