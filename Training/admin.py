from django.contrib import admin


from Training.models import AdvancedTraining, BasicTraining, Enquireform


@admin.register(AdvancedTraining)
class AdvancedTrainingAdmin(admin.ModelAdmin):
    list_display=['id','rest','roll', 'salute','Resttodown', 'hifi','longstay',]

@admin.register(BasicTraining)
class BasicTrainingAdmin(admin.ModelAdmin):
    list_display=['id','heelwalk','down','stop','downtosit',]


@admin.register(Enquireform)
class Enquireform(admin.ModelAdmin):
    list_display=['id','personname','phone_no','email','petname','Address',]    
    