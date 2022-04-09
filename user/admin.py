import site
from tkinter.ttk import Style
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.db import models
# from django.utils.html import format_html

# Register your models here.
from .models import  Users,AbstractUser, Profileinfo
# admin.site.site_title="PETISHH ADMIN"
# admin.site.site_url="http://petishh.com"
admin.site.site_header = "PETISHH ADMIN" 
# admin.site.index_title="Petishh Administration"
admin.site.index_title="Petishh Administration"
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']
# @admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display=['id','email', 'username','phone_no','profile_image','is_staff', 'is_superuser']
    list_filter = ('is_staff', 'is_superuser', 'is_deleted',)
    list_display_links = ('id','email', 'username',)

admin.site.register(Users,UsersAdmin)    
    
# def add(self, add):
#     return format_html(f'<a href="/admin/account/emailaddress/add/" class="addlink" Style="color:red">Add</a>')    



# @admin.register(Users)
# class UsersAdmin(admin.ModelAdmin):
#     list_display=['id','email','username','phone_no','last_login','is_staff','is_active','is_superuser',]


# @admin.register(OTP)
# class OTPAdmin(admin.ModelAdmin):
#     list_display=['id','user','otp',]


# @admin.register(EmailCodeVerification)
# class EmailCodeverificationAdmin(admin.ModelAdmin):
#     list_dispaly=['id','user', 'email', 'verification',]    

# @admin.register(Profileinfo)
# class Profileinfo(admin.ModelAdmin):
#     list_display=['id', 'user']


# from django.contrib.sites.models import Site

# # admin.site.register(Site)
# admin.site.unregister(Site)    