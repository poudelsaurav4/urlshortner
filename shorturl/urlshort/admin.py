from django.contrib import admin

# Register your models here.
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.register(CustomUser)
# admin.site.register(RegisterUser)

# class User_detailsInline(admin.StackedInline):
#     model = User_details
#     verbose_name_plural = 'user_details'

# class UserAdmin(BaseUserAdmin):
#     inlines = [User_detailsInline]

# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
admin.site.register(UrlData)