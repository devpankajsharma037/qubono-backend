from django.contrib import admin
from .models import User,Token,IPAddress
from django.contrib.auth.models import Group

admin.site.unregister(Group)

class UserAdmin(admin.ModelAdmin):
    list_display    = ['id', 'first_name', 'last_name','email','role','is_active','is_delete']
    list_filter     = ['is_active','email','role']
    search_fields   = ['first_name', 'last_name', 'email' ,'role']
admin.site.register(User, UserAdmin)

class TokenAdmin(admin.ModelAdmin):
    list_display = ['id','user','type','token']
admin.site.register(Token, TokenAdmin)

class IPAddressAdmin(admin.ModelAdmin):
    list_display = ['id']
admin.site.register(IPAddress, IPAddressAdmin)