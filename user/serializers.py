from ast import arg
import base64
from os import write
from pyexpat import model
from tkinter import filedialog
from turtle import right

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import Group, GroupManager
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from django.conf import settings
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from user.models import *
from datetime import datetime
from django.contrib.auth.models import User
from fcm_django.models import FCMDevice
from django.db.models.signals import post_save
User = get_user_model()



# //////////////////////////// Customer login reg ///////////////////////////////
class RegistrationSerializer(serializers.ModelSerializer):
    email= serializers.EmailField(max_length=50, min_length=6 )
    username=serializers.CharField(max_length=50, min_length=6)
    password=serializers.CharField(max_length=150, write_only=True)
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password']
    
    def validate(self, args):
        email=args.get('email', None)
        username=args.get('username', None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email':('email already exists')})
        if User.objects.filter(username=username).exists():
                raise serializers.ValidationError({'username':('username already exists')})
        return super().validate(args)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)   


class CustomerSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, allow_blank=False, max_length=200)
    phone_no = serializers.CharField(required=True, allow_blank=False, max_length=20)
    email = serializers.CharField(required=True, allow_blank=False, max_length=200)
     

    class Meta:
        model = get_user_model()
        fields = ['email', 'username','phone_no', 'password',]

class CustomerLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True, write_only=True)
    email = serializers.CharField(required=False, write_only=True, label="Email Address")
    phone_no = serializers.CharField(required=False, write_only=True, max_length=10, label="Mobile Number")
    token = serializers.CharField(allow_blank=True, read_only=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    class Meta(object):
        many = True
        model = get_user_model()
        fields = ['id', 'phone_no', 'email', 'username', 'password', 'token', 'first_name', 'last_name', 'is_superuser', 'is_active', 'is_staff', 'last_login']

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True, write_only=True)
    email = serializers.EmailField(required=True, write_only=True, label="Email Address")
    phone_no = serializers.CharField(required=True, write_only=True, max_length=10, label="Mobile Number")
    token = serializers.CharField(allow_blank=True, read_only=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    class Meta(object):
        many = True
        model = get_user_model() 
        fields = ['id', 'phone_no', 'email', 'username', 'password', 'token', 'first_name', 'last_name', 'email',
                  'is_superuser', 'is_active', 'is_staff', 'last_login']

class LoginOtpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True, write_only=True)
    phone_no = serializers.CharField(required=True, write_only=True, max_length=10, label="Mobile Number")
    token = serializers.CharField(allow_blank=True, read_only=True)

    class Meta(object):
        many = True
        model = Users
        fields = ['id', 'phone_no', 'email', 'username', 'password', 'token', 'first_name', 'last_name', 'email',
                  'is_superuser', 'is_active', 'is_staff', 'last_login']



class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, allow_blank=False, max_length=200)
    phone_no = serializers.CharField(required=True, allow_blank=False, max_length=20)
    email = serializers.CharField(required=True, allow_blank=False, max_length=200)
    first_name = serializers.CharField(required=True, allow_blank=False, max_length=200)
    last_name = serializers.CharField(required=True, allow_blank=False, max_length=200)
    

    class Meta:
        model = get_user_model()
        fields = ['email', 'phone_no', 'password', 'first_name', 'last_name']
        
        
class SignupSellerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, allow_blank=False, max_length=200)
    last_name = serializers.CharField(required=True, allow_blank=False, max_length=200)
    name = serializers.CharField(required=True, allow_blank=False, max_length=200)
    password = serializers.CharField(required=True, allow_blank=False, max_length=200)
    phone_no = serializers.CharField(required=True, allow_blank=False, max_length=20)
    email = serializers.CharField(required=True, allow_blank=False, max_length=200)
    shop_name = serializers.CharField(required=True, allow_blank=False, max_length=200)
    shop_city = serializers.CharField(required=True, allow_blank=False, max_length=200)
    state = serializers.CharField(required=True, allow_blank=False, max_length=200)
    referel_code = serializers.CharField(required=True, allow_blank=True, max_length=200)
    
    class Meta:
        model = Users
        fields = ['email', 'phone_no', 'password','shop_name','shop_city','state','referel_code','name','first_name','last_name']


class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"


class SellerProfileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profileinfo
        fields = "__all__"

class SellerProfileInfoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profileinfo
        fields = "__all__"


class EmailViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailCodeVerification
        fields ="__all__"


class MobileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = "__all__"

class AccountViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['phone_no']


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'phone_no', 'first_name', 'last_name','profile_image','home_address','address']

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    new_password = serializers.CharField(required=True)



class FireBaseDeviceAccess(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = "__all__"


class NotificationMsg(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=68,write_only=True)
    token = serializers.CharField(min_length=1)
    uidb64 = serializers.CharField(min_length=1)

    class Meta:
        fields = ['password']

class ProfileinfoSerializer(serializers.Serializer):
    class Meta:
        model = Profileinfo
        fields= "__all__"


class SocialSerializer(serializers.Serializer):
# """
# Serializer which accepts an OAuth2 access token and provider.
# """
    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)        





from django.contrib.auth import authenticate, get_user_model
from djoser.conf import settings
from djoser.serializers import TokenCreateSerializer

User = get_user_model()

class CustomTokenCreateSerializer(TokenCreateSerializer):

    def validate(self, attrs):
        password = attrs.get("password")
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )
        if not self.user:
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        # We changed only below line
        if self.user: # and self.user.is_active: 
            return attrs
        self.fail("invalid_credentials")    




from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = Users
        fields = ['email', 'username', 'password', 'phone_no']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return Users.objects.create_user(**validated_data)     

from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

class EmailVerificationSerializer(serializers.ModelSerializer):
    token= serializers.CharField(max_length=555)

    class Meta:
        model = Users
        fields =['tokens']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3,read_only=True)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3)

    tokens = serializers.SerializerMethodField()
    class Meta:
        model = Users
        fields = ['email', 'password', 'username', 'tokens']

    def get_tokens(self, obj):
        user = Users.objects.get(username=obj['username'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }



    def validate(self, attrs):
        email=attrs.get('email', '')
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(username=username, password=password)
        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }



class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_tokne': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.tokens = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.tokens).blacklist()

        except TokenError:
            self.fail('bad_token')