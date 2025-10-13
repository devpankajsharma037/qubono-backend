from django.contrib import admin
from .models import User,Token
from django.contrib.auth.models import Group
from django.utils.html import format_html

admin.site.unregister(Group)

class UserAdmin(admin.ModelAdmin):
    list_display    = ['id', 'first_name', 'last_name','email','role','is_active','is_delete']
    list_filter     = ['is_active','email','role']
    search_fields   = ['first_name', 'last_name', 'email' ,'role']
admin.site.register(User, UserAdmin)

class TokenAdmin(admin.ModelAdmin):
    list_display = ['id','users','type','token','is_deleted','is_active']

    def users(self, obj):
        if obj.user:
            return format_html(
                "<a href='/admin/customer/user/{}/change/'>{}</a>",obj.user.id,obj.user
            )
        return "-"
    users.short_description = "User"

admin.site.register(Token, TokenAdmin)