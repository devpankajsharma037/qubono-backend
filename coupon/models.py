from django.db import models
from customer.models import User
from core.utils.commonModel import CommonModel

class Merchant(CommonModel):
    name    = models.CharField(max_length=100,blank=True,null=True)
    logo    = models.ImageField(upload_to="/media",blank=True,null=True)
    banner  = models.ImageField(upload_to="/media",blank=True,null=True)