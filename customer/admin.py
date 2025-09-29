from django.contrib import admin
from .models import User,Token

class UserAdmin(admin.ModelAdmin):
    list_display    = ['id', 'first_name', 'last_name','email','role']
    list_filter     = ['is_active','email','role']
    search_fields   = ['first_name', 'last_name', 'email']
admin.site.register(User, UserAdmin)

class TokenAdmin(admin.ModelAdmin):
    list_display = ['id','user','token']
admin.site.register(Token, TokenAdmin)