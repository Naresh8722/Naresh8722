# from django.db import models

# # Create your models here.
# class phoneModel(models.Model):
#     Mobile = models.IntegerField(blank=False)
#     isVerified = models.BooleanField(blank=False, default=False)
#     counter = models.IntegerField(default=0, blank=False)
# def __str__(self):
#         return str(self.Mobile)



from django.db import models
from django.db.models.fields import EmailField
from django.utils.translation import deactivate
from django.utils.html import mark_safe
# Doctor Booking Slot
class Appointment(models.Model):
    """Contains info about appointment"""

    class Meta:
        unique_together = ('doctor', 'date', 'timeslot')

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
    boarding_Choice=(('Dog Boarding','Dog Boarding'),
                    ('Dog Kennels', 'Dog Kennels'),
                    ('Cat Boarding', 'Cat Boarding'),
                    ('Doggy Daycare', 'Doggy Daycare'),
                    ('Pet Hotels','Pet Hotels'),
                    ('Private Pet Boarding','Private Pet Boarding'))

    first_name= models.CharField(max_length=25,default="", null=True )
    last_name=models.CharField(max_length=10, default="", null=True)
    address=models.CharField(max_length=255, default="", null=True)
    email= models.EmailField(null=True)
    phone_no=models.CharField(max_length=12, default="", null=True)
    doctor = models.ForeignKey('Doctor',on_delete = models.CASCADE)
    date = models.DateField(help_text="DD-MM-YYYY")
    timeslot = models.IntegerField(choices=TIMESLOT_LIST)
    boarding= models.CharField(max_length=60,choices=boarding_Choice,default="")
    message=models.CharField(max_length=255, default="", null=True)

    def __str__(self):
        return '{} {} {}. Patient: {}'.format(self.date, self.time, self.doctor, self.first_name)

    @property
    def time(self):
        return self.TIMESLOT_LIST[self.timeslot][1]


class Doctor(models.Model):
    """Stores info about doctor"""

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    image = models.FileField()
    middle_name = models.CharField(max_length=20)
    specialty = models.CharField(max_length=20)

    def __str__(self):
        return '{} {}'.format(self.specialty, self.short_name)
 
    def image_tag(self):
        return mark_safe('<img src="%s" width="40" height="40" />' % (self.image.url))

    image_tag.short_description = 'Image'
    image_tag.allow=True        

    @property
    def short_name(self):
        return '{} {}.{}'.format(self.last_name.title(), self.first_name[0].upper(), self.middle_name[0].upper())