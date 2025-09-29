from django.contrib import admin
from .models import Merchant,Deal


class MerchantAdmin(admin.ModelAdmin):
    list_display = ['id','user']
admin.site.register(Merchant, MerchantAdmin)

class DealAdmin(admin.ModelAdmin):
    list_display = ['id','user']
admin.site.register(Deal, DealAdmin)