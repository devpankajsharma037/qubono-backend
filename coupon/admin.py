from django.contrib import admin
from .models import Store,Category,SubCategory,Coupon,Wishlist,Notification


commanList = ['user', 'is_deleted', 'is_active']

class StoreAdmin(admin.ModelAdmin):
    list_display = ['id','slug', 'name','website_url'] + commanList
admin.site.register(Store, StoreAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id'] + commanList
admin.site.register(Category, CategoryAdmin)

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id'] + commanList
admin.site.register(SubCategory, SubCategoryAdmin)

class CouponAdmin(admin.ModelAdmin):
    list_display = ['id',"type","store"] + commanList
admin.site.register(Coupon, CouponAdmin)

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['id'] + commanList
admin.site.register(Wishlist, WishlistAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id'] + commanList
admin.site.register(Notification, NotificationAdmin)