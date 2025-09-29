from django.contrib import admin
from .models import Merchant


class MerchantAdmin(admin.ModelAdmin):
    list_display = ['id','user']
admin.site.register(Merchant, MerchantAdmin)