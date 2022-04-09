# from typing import ClassVar, Generic
from django.db import models
# from django.db.models.base import Model
# from django.db.models.enums import Choices
# from django.db.models.fields import _Choice
# from django.utils.translation import deactivate

class Hygienicpamper(models.Model):
    bathandShampoo=models.BooleanField(default=True)
    towelandblowdry=models.BooleanField(default=True)
    perfumesparay=models.BooleanField(default=True)
    deshedding=models.BooleanField(default=True)
    nailtrimming=models.BooleanField(default=True)
    earcleaning=models.BooleanField(default=True)
    theethcleaning=models.BooleanField(default=True)
    price=models.PositiveIntegerField()
    discountprice=models.PositiveIntegerField()
    class Meta:
        db_table='Hygienicpamper'


class Bugrecue(models.Model):
    
    tickandfleatreatment=models.BooleanField(default=True)        
    towelandblowdry=models.BooleanField(default=True)
    perfumesparay=models.BooleanField(default=True)
    deshedding=models.BooleanField(default=True)
    nailtrimming=models.BooleanField(default=True)
    earcleaning=models.BooleanField(default=True)
    theethcleaning=models.BooleanField(default=True)
    pawmassage=models.BooleanField(default=True)
    medicatedbath=models.BooleanField(default=True)
    price=models.PositiveIntegerField()
    discountprice=models.PositiveIntegerField()
    class Meta:
        db_table="Bugrecue"


class Happyandshiny(models.Model):
    bathandShampoo=models.BooleanField(default=True)       
    towelandblowdry=models.BooleanField(default=True)
    perfumesparay=models.BooleanField(default=True)
    deshedding=models.BooleanField(default=True)
    nailtrimming=models.BooleanField(default=True)
    earcleaning=models.BooleanField(default=True)
    theethcleaning=models.BooleanField(default=True)
    pawmassage=models.BooleanField(default=True)
    Hairtrimiming=models.BooleanField(default=True)
    price=models.PositiveIntegerField()
    discountprice=models.PositiveIntegerField()
    class Meta:
        db_table="happyandshiny"

class Shinyandbugfree(models.Model):
    titel=models.CharField(max_length=200, default="", null=True)
    bathandShampoo=models.BooleanField(default=True) 
    perfumesparay=models.BooleanField(default=True)       
    towelandblowdry=models.BooleanField(default=True)
    # perfumesparay=models.BooleanField(default=True)
    deshedding=models.BooleanField(default=True)
    nailtrimming=models.BooleanField(default=True)
    earcleaning=models.BooleanField(default=True)
    theethcleaning=models.BooleanField(default=True)
    pawmassage=models.BooleanField(default=True)
    Hairtrimiming=models.BooleanField(default=True)
    price=models.PositiveIntegerField('Shinyandbugfree price' )
    # discountprice=models.PositiveIntegerField()
    class Meta:
        db_table="shinyandbugfree"
    def __str__(self) :
        return self.titel







# class Booking(models.Model):
#     Gender_Choice= (('M', 'Male'),
#                     ('F', 'Female'))
#     Petname_Choice=(('D', 'Dog'),
#                     ('C', 'Cat'),
#                     ('O', 'Other'))

#     personname= models.CharField(max_length=60, default="", null=True)
#     phone_no=models.CharField(max_length=13, default="", null=True)
#     email= models.EmailField(null=True)
#     Address=models.CharField(max_length=200, default="" , null=True)
#     country= models.CharField(max_length=50, default="", null =True)
#     state=models.CharField(max_length=60, default="", null=True)
#     city=models.CharField(max_length=100, default="", null= True)
#     zipcode=models.PositiveIntegerField()

#     petname=models.CharField(max_length=10,
#                     choices=Petname_Choice,
#                     default="" )
#     gender= models.CharField(max_length=9,
#                   choices=Gender_Choice,
#                   default="")

#     upload = models.FileField()
#     groomingkit=models.CharField(max_length=50, default="", null=True)
 




class GroomerBookingslot(models.Model):
    """Contains info about appointment"""

    class Meta:
        unique_together = ('groomer', 'date', 'timeslot')

    TIMESLOT_LIST = (
        (0, '09:00 – 09:30'),
        (1, '10:00 – 10:30'),
        (2, '11:00 – 11:30'),
        (3, '12:00 – 12:30'),
        (4, '13:00 – 13:30'),
        (5, '14:00 – 14:30'),
        (6, '15:00 – 15:30'),
        (7, '16:00 – 16:30'),
        (8, '17:00 – 17:30'),
    )

    Gender_Choice= (('M', 'Male'),
                    ('F', 'Female'))
    Petname_Choice=(('D', 'Dog'),
                    ('C', 'Cat'),
                    ('O', 'Other'))
    first_name= models.CharField(max_length=25,default="", null=True )
    last_name=models.CharField(max_length=10, default="", null=True)
    address=models.CharField(max_length=255, default="", null=True)
    email= models.EmailField(null=True)
    phone_no=models.CharField(max_length=12, default="", null=True)
    groomer = models.ForeignKey('Groomer',on_delete = models.CASCADE)
    date = models.DateField(help_text="DD-MM-YYYY")
    timeslot = models.IntegerField(choices=TIMESLOT_LIST)
    patient_name = models.CharField(max_length=60)
    petname=models.CharField(max_length=10,
                    choices=Petname_Choice,
                    default="" )
    gender= models.CharField(max_length=9,
                  choices=Gender_Choice,
                  default="")
    message=models.CharField(max_length=255, default="", null=True)

    def __str__(self):
        return '{} {} {}. Patient: {}'.format(self.date, self.time, self.groomer, self.patient_name)

    @property
    def time(self):
        return self.TIMESLOT_LIST[self.timeslot][1]


class Groomer(models.Model):
    """Stores info about Groomer"""

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    specialty = models.CharField(max_length=20)

    def __str__(self):
        return '{} {}'.format(self.specialty, self.short_name)

    @property
    def short_name(self):
        return '{} {}.{}.'.format(self.last_name.title(), self.first_name[0].upper(), self.middle_name[0].upper())