from django.contrib import admin
from .models import Payment,Order,CouponUsage

class PaymentAdmin(admin.ModelAdmin):
    list_display    = ['id']
admin.site.register(Payment, PaymentAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id',]
admin.site.register(Order, OrderAdmin)

class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ['id',]
admin.site.register(CouponUsage, CouponUsageAdmin)