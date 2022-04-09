from django.contrib import admin
from django.contrib.admin.filters import ListFilter

from Doctor.models import Doctor, Appointment


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display=['id','first_name', 'middle_name','last_name', 'specialty','image_tag']
    list_filter=('first_name', 'last_name', 'specialty')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display=('id','doctor','first_name', 'last_name', 'phone_no', 'timeslot', 'date',)
    list_filter=('first_name', 'last_name', 'phone_no', 'timeslot', 'date','doctor', )
    