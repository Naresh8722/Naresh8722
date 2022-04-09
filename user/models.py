from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from datetime import datetime
from django.utils import timezone
# from petishh.custom_users import permissions
from user.utils import SoftDeleteManager
from fcm_django.models import FCMDevice


from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
import smtplib,ssl
from email.message import EmailMessage

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
 
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    return True

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}
# Create your models here.

class Users(AbstractUser):
    # username = models.CharField(max_length = 50, blank = True, null = True, unique = True) 
    referelcode = models.CharField(max_length=20, default="", blank=True)
    refererid = models.CharField(max_length=20, default="", blank=True,null=True)
    wallet = models.IntegerField(default=0)
    dateofbirth = models.CharField(max_length=20, default="", blank=True)
    adhaarcard = models.CharField(max_length=20, default="", blank=True)
    pancard = models.CharField(max_length=20, default="", blank=True)
    pancardtype = models.CharField(max_length=20, default="", blank=True)
    phone_no = models.CharField(max_length=20, default="", blank=True)
    secondary_no = models.CharField(max_length=20, default="", blank=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=True, verbose_name='Phone Verification')
    # is_email_verified = models.BooleanField(default=True, verbose_name='Email Verification')
    # verified_code = models.CharField(max_length=500)
    reset_password = models.BooleanField(default=False)
    address = models.CharField(max_length=255, default="", blank=True, null=True)
    home_address = models.CharField(max_length=255, default="", blank=True, null=True)
    profile_image = models.CharField(max_length=225, blank=True, null=True)
    latitude = models.CharField(max_length=255, null=True)
    longitude = models.CharField(max_length=255, null=True)
    created_date = models.DateTimeField(default=datetime.now, blank=True)
    modified_date = models.DateTimeField(default=datetime.now, blank=True)
    is_blocked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    shop_name = models.CharField(max_length=255, blank=True, null=True)
    gstin_present = models.CharField(max_length=255, blank=True, null=True)
    gstin_number = models.CharField(max_length=255, blank=True, null=True)
    registration_date = models.DateTimeField(null=True, blank=True)
    gst_state = models.CharField(max_length=255, blank=True, null=True)
    gst_type = models.CharField(max_length=255, blank=True, null=True)

    shop_city = models.CharField(max_length=255, blank=True, null=True)
    shop_landmark = models.CharField(max_length=255, null=True)
    pin_code = models.IntegerField(default=0, null=True)
    shop_image = models.CharField(max_length=225, blank=True, null=True)
    aadhaar_front_image = models.CharField(max_length=225, blank=True, null=True)
    gstin_image = models.CharField(max_length=225, blank=True, null=True)

    user_type = models.IntegerField(default=0, null=True)
    account  = models.CharField(max_length=225, blank=True, null=True)
    is_shop_verified = models.BooleanField(default=False)
    aadhaar_back_image = models.CharField(max_length=225, blank=True, null=True)
    owner_image = models.CharField(max_length=225, blank=True, null=True)
    floor_no = models.IntegerField(default=0, null=True)
    mall_name = models.CharField(max_length=225, blank=True, null=True)
    state = models.CharField(max_length=225, blank=True, null=True)
    shop_area = models.CharField(max_length=225, blank=True, null=True)
    shop_comment = models.CharField(max_length=225, blank=True, null=True)
    owner_comment = models.CharField(max_length=225, blank=True, null=True)
    gstin_comment = models.CharField(max_length=225, blank=True, null=True)
    aadhar_front_comment = models.CharField(max_length=225, blank=True, null=True)
    aadhar_back_comment = models.CharField(max_length=225, blank=True, null=True)
    is_submitted =models.BooleanField(default=False)
    pancard_image = models.CharField(max_length=225, blank=True, null=True)
    driving_license = models.CharField(max_length=25, default="", blank=True) # New added
    driving_license_image = models.CharField(max_length=225, blank=True, null=True) # new added
    current_address_proof = models.CharField(max_length=225, blank=True, null=True) # new added
    rtpcr_certificate = models.CharField(max_length=225, blank=True, null=True) # new added
    valid_from = models.DateField(null=True) # new added
    valid_upto = models.DateField(null=True) # new added
    is_auth =models.BooleanField(default=False)
    status =models.BooleanField(default=False)
    comment = models.CharField(max_length=500, blank=True, null=True)    
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    # objects = UserManager()
    class Meta:
        db_table = 'auth_user'

    def get_name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.username
        
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }    

    # Mobile otp Verification


class OTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_otp')
    mobile = models.CharField(max_length=15, blank=True, null=True)
    otp = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=datetime.now, blank=True)
    modified_date = models.DateTimeField(default=datetime.now, blank=True)
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'otp'
    def __str__(self):
        return self.mobile


class EmailCodeVerification(models.Model):
	user 			    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_verification')
	email 			    = models.CharField(max_length=255, blank=True, null=True)
	verification_code   = models.CharField(max_length=500, blank=True, null=True)
	is_varified 		= models.BooleanField(default=False)
	is_deleted 			= models.BooleanField(default=False)
	created_date 		= models.DateTimeField(default=datetime.now, blank=True)
	modified_date 		= models.DateTimeField(default=datetime.now, blank=True)



class Notification(models.Model):
	user 			    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_notification')
	message 			= models.CharField(max_length=255, blank=True, null=True)
	title               = models.CharField(max_length=255, blank=True, null=True)
	is_opened 		    = models.BooleanField(default=False)
	icon_image 			= models.CharField(max_length=255, blank=True, null=True)
	datamsg 		    = models.CharField(max_length=255, blank=True, null=True)
	created_date 		= models.DateTimeField(default=datetime.now, blank=True)


class Profileinfo(models.Model):
    user 			    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile_info',null=True)
    Information         = models.TextField(blank=True, null=True)
    philisophy          = models.TextField(blank=True, null=True)
    achievements        = models.TextField(blank=True, null=True)
    toprecipe           = models.TextField(blank=True, null=True)

    image1              = models.CharField(max_length=225, blank=True, null=True)
    image2              = models.CharField(max_length=225, blank=True, null=True)
    image3              = models.CharField(max_length=225, blank=True, null=True)
    image4              = models.CharField(max_length=225, blank=True, null=True)
    image5              = models.CharField(max_length=225, blank=True, null=True)
    image6              = models.CharField(max_length=225, blank=True, null=True)
    image7              = models.CharField(max_length=225, blank=True, null=True)
    image8              = models.CharField(max_length=225, blank=True, null=True)
    image9              = models.CharField(max_length=225, blank=True, null=True)
    image10             = models.CharField(max_length=225, blank=True, null=True)
    selectedimage1 = models.IntegerField(default=1, null=True)
    selectedimage2 = models.IntegerField(default=3, null=True)
    selectedimage3 = models.IntegerField(default=5, null=True)
    selectedimage4 = models.IntegerField(default=7, null=True)
    selectedimage5 = models.IntegerField(default=9, null=True)
    is_approved = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'profile'

class StaticSubscribe(models.Model):
    email = models.EmailField(max_length=255, blank=True, null=True)




from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False
 


    