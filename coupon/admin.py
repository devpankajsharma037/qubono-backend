from django.contrib import admin
from .models import Merchant,Deal,Category,SubCategory


class MerchantAdmin(admin.ModelAdmin):
    list_display = ['id','user']
admin.site.register(Merchant, MerchantAdmin)

class DealAdmin(admin.ModelAdmin):
    list_display = ['id','user']
admin.site.register(Deal, DealAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id']
admin.site.register(Category, CategoryAdmin)

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id']
admin.site.register(SubCategory, SubCategoryAdmin)