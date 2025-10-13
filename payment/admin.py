from django.contrib import admin
from .models import Payment,Order,CouponUsage
from django.utils.html import format_html

commanList = ['is_deleted', 'is_active']

class PaymentAdmin(admin.ModelAdmin):
    list_display    = ['id','users','status','price','platform_name','order_id',] + commanList

    def users(self, obj):
        if obj.user:
            return format_html(
                "<a href='/admin/customer/user/{}/change/'>{}</a>",obj.user.id,obj.user
            )
        return "-"
    users.short_description = "User"
admin.site.register(Payment, PaymentAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','users','coupons','payments','order_id','total_amount','discount_amount','final_amount'] + commanList

    def payments(self, obj):
        if obj.payment:
            return format_html(
                "<a href='/admin/payment/payment/{}/change/'>view payment</a>",obj.payment.id,
            )
        return "-"
    payments.short_description = "Payment"

    def coupons(self, obj):
        if obj.coupon:
            return format_html(
                "<a href='/admin/coupon/coupon/{}/change/'>View coupon</a>",obj.coupon.id,
            )
        return "-"
    coupons.short_description = "Coupon"

    def users(self, obj):
        if obj.user:
            return format_html(
                "<a href='/admin/customer/user/{}/change/'>{}</a>",obj.user.id,obj.user
            )
        return "-"
    users.short_description = "User"
admin.site.register(Order, OrderAdmin)

class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ['id','coupons','users','orders','used_at'] + commanList

    def coupons(self, obj):
        if obj.coupon:
            return format_html(
                "<a href='/admin/coupon/coupon/{}/change/'>View coupon</a>",obj.coupon.id,
            )
        return "-"
    coupons.short_description = "Coupon"

    def users(self, obj):
        if obj.user:
            return format_html(
                "<a href='/admin/customer/user/{}/change/'>{}</a>",obj.user.id,obj.user
            )
        return "-"
    users.short_description = "User"

    def orders(self, obj):
        if obj.order:
            return format_html(
                "<a href='/admin/payment/order/{}/change/'>View order</a>",obj.order.id
            )
        return "-"
    orders.short_description = "Order"
admin.site.register(CouponUsage, CouponUsageAdmin)