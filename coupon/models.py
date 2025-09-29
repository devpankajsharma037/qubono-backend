from django.db import models
from customer.models import User
from core.utils.commonModel import CommonModel

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