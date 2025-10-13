from django.contrib import admin
from .models import (Store,Category,SubCategory,Coupon,Wishlist,Notification,Rating)
from django.utils.html import format_html

commanList = ['is_deleted', 'is_active']

class StoreAdmin(admin.ModelAdmin):
    list_display = ['id','slug', 'name','website_url','users'] + commanList

    def users(self, obj):
        if obj.user:
            return format_html(
                "<a href='/admin/customer/user/{}/change/'>{}</a>",obj.user.id,obj.user
            )
        return "-"
    users.short_description = "Created by"
admin.site.register(Store, StoreAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','users','is_popular','is_premium'] + commanList

    def users(self, obj):
        if obj.user:
            return format_html(
                "<a href='/admin/customer/user/{}/change/'>{}</a>",obj.user.id,obj.user
            )
        return "-"
    users.short_description = "Created by"


admin.site.register(Category, CategoryAdmin)

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','users','categorys','is_popular','is_premium'] + commanList
    
    def categorys(self, obj):
        if obj.category:
            return format_html(
                "<a href='/admin/coupon/category/{}/change/'>View category</a>",obj.category.id
            )
        return "-"
    categorys.short_description = "Categorys"

    def users(self, obj):
        if obj.user:
            return format_html(
                "<a href='/admin/customer/user/{}/change/'>{}</a>",obj.user.id,obj.user
            )
        return "-"
    users.short_description = "Created by"
admin.site.register(SubCategory, SubCategoryAdmin)

class CouponAdmin(admin.ModelAdmin):
    list_display = ['id','name',"type","users","stores"] + commanList

    def users(self, obj):
        if obj.user:
            return format_html(
                "<a href='/admin/customer/user/{}/change/'>{}</a>",obj.user.id,obj.user
            )
        return "-"
    users.short_description = "Created by"

    def stores(self, obj):
        if obj.store:
            return format_html(
                "<a href='/admin/coupon/store/{}/change/'>View store</a>",obj.store.id
            )
        return "-"
    stores.short_description = "Store"
admin.site.register(Coupon, CouponAdmin)

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['id','users','stores'] + commanList

    def stores(self, obj):
        if obj.store:
            return format_html(
                "<a href='/admin/coupon/store/{}/change/'>View Store</a>",obj.store.id,
            )
        return "-"
    stores.short_description = "Store"

    def users(self, obj):
        if obj.user:
            return format_html(
                "<a href='/admin/customer/user/{}/change/'>{}</a>",obj.user.id,obj.user
            )
        return "-"
    users.short_description = "User"
admin.site.register(Wishlist, WishlistAdmin)

# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ['id'] + commanList
# admin.site.register(Notification, NotificationAdmin)

class RatingAdmin(admin.ModelAdmin):
    list_display = ['id','title','users','stores','is_approved','rating'] + commanList

    def users(self, obj):
        if obj.user:
            return format_html(
                "<a href='/admin/customer/user/{}/change/'>{}</a>",obj.user.id,obj.user
            )
        return "-"
    users.short_description = "Given by"

    def stores(self, obj):
        if obj.store:
            return format_html(
                "<a href='/admin/coupon/store/{}/change/'>View store</a>",obj.store.id
            )
        return "-"
    stores.short_description = "Store"

admin.site.register(Rating, RatingAdmin)