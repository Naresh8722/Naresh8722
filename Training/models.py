from typing import ClassVar, Generic
from django.db import models
from django.db.models.base import Model
from django.db.models.enums import Choices
# from django.db.models.fields import _Choice
from django.utils.translation import deactivate

class AdvancedTraining(models.Model):
    rest=models.BooleanField(default=True)
    roll=models.BooleanField(default=True)
    salute=models.BooleanField(default=True)
    Resttodown=models.BooleanField(default=True)
    hifi=models.BooleanField(default=True)
    longstay=models.BooleanField(default=True)
    fetch=models.BooleanField(default=True)
    crawl=models.BooleanField(default=True)
    class Meta:
        db_table='AdvancedTraining'

    def __bool__(self):
        return self.rest
class BasicTraining(models.Model):
    heelwalk=models.BooleanField(default=True)        
    down=models.BooleanField(default=True)
    stop=models.BooleanField(default=True)
    downtosit=models.BooleanField(default=True)
    sit=models.BooleanField(default=True)
    shakehand=models.BooleanField(default=True)
    standstay=models.BooleanField(default=True)
    distancecontrol=models.BooleanField(default=True)
    come=models.BooleanField(default=True)
    class Meta:
        db_table='BasicTraining'

    def __bool__(self):
        return self.heelwalk

class Enquireform(models.Model):
    Gender_Choice= (('M', 'Male'),
                    ('F', 'Female'))
    Petname_Choice=(('D', 'Dog'),
                    ('C', 'Cat'),
                    ('O', 'Other'))
    Training_choice =(('BasicTraining','BasicTraining'),
                        ('AdvancedTraining',' AdvancedTraining'))              

    personname= models.CharField(max_length=60, default="", null=True)
    phone_no=models.CharField(max_length=13, default="", null=True)
    email= models.EmailField(null=True)
    Address=models.CharField(max_length=200, default="" , null=True)
    country= models.CharField(max_length=50, default="", null =True)
    state=models.CharField(max_length=60, default="", null=True)
    city=models.CharField(max_length=100, default="", null= True)
    zipcode=models.IntegerField()

    petname=models.CharField(max_length=10,
                    choices=Petname_Choice,
                    default="" )
    gender= models.CharField(max_length=9,
                  choices=Gender_Choice,
                  default="")

    upload = models.FileField()
    trainingkit=models.CharField(max_length=50,choices=Training_choice, default="")

    def __str__(self):
        return self.personname

