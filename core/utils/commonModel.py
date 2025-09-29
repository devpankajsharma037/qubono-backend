from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import models
import uuid


class CommonModel(models.Model):
    id          = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False, db_index=True, unique=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    is_deleted  = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=False)
    class Meta:
        abstract = True
