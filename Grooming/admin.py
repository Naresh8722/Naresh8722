from django.contrib import admin
from .models import Hygienicpamper, Bugrecue,Happyandshiny, Shinyandbugfree,  Groomer,GroomerBookingslot

@admin.register(Hygienicpamper)
class HygienicpamperAdmin(admin.ModelAdmin):
    list_display=['price','discountprice']

@admin.register(Bugrecue)
class BugrecueAdmin(admin.ModelAdmin):
    list_display=['price','discountprice']


@admin.register(Happyandshiny)
class HappyandshinyAdmin(admin.ModelAdmin):
    list_display=['price', 'discountprice']    



@admin.register(Shinyandbugfree)
class ShinyandbugfreeAdmin(admin.ModelAdmin):
    list_display=['price',] 
    
     



# @admin.register(Booking)
# class BookingAdmin(admin.ModelAdmin):
#     list_display=[all]    


@admin.register(Groomer)
class GroomerAdmin(admin.ModelAdmin):
    list_display=['id','first_name','specialty',]    


@admin.register(GroomerBookingslot)
class GroomerBookingslotAdmin(admin.ModelAdmin):
    list_display=['id','first_name', 'last_name', 'phone_no', 'groomer','timeslot',]  
    list_filter = ('patient_name','phone_no','groomer', 'timeslot','date')
    # actions_on_bottom = True