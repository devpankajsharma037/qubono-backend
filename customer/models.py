import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from core.utils.commonModel import CommonModel

class Role(models.TextChoices):
    ADMIN     = "ADMIN",
    EMPLOYEE  = "EMPLOYEE",

class User(AbstractUser):
    id      = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,unique=True)
    role    = models.CharField(max_length=20,choices=Role.choices,default=Role.EMPLOYEE)


class Type(models.TextChoices):
    OTP              = "OTP",
    FORGOT_PASSWORD  = "FORGOT_PASSWORD",

class Token(CommonModel):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    type    = models.CharField(max_length=20,choices=Type.choices,default=Type.OTP)
    token   = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        verbose_name_plural = 'Token'
