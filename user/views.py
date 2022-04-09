from ast import Expression
import email
from email.policy import HTTP
import http
from json import JSONEncoder
from lib2to3.pgen2 import token
from msilib.schema import SelfReg
from tkinter import ACTIVE
from unicodedata import name
from urllib import response
import uuid
from django.shortcuts import render

from .forms import CommentForm
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib,ssl
from .models import StaticSubscribe
from email.message import EmailMessage


def comingsoon(request):
    if request.method== 'GET':
        return render(request, 'coming-soon.html')
    else:
      mail = request.POST.get("email")
      check = StaticSubscribe.objects.filter(email=mail).count()
      sent =send_mail_otp(mail)
      form= CommentForm(request.POST)
      if form.is_valid():
        form.save()
        mail = request.POST.get("email")
        if sent:
          form = CommentForm()
          return render(request, 'coming-soon.html')
        else:
          return render(request, 'coming-soon.html',{"c":"Invalid Email"})






def send_mail_otp(receiver_mail):
    msg = EmailMessage()
    msg['Subject'] = 'Thanking for Subscribing us '
    msg['From'] = "no-reply@bakeapp.naresh@thorsignia.online" 
    msg['To'] = receiver_mail
    msg.set_content('''
    <!DOCTYPE html>
    <html>
        <head>
          <!-- Required meta tags -->
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <!-- Bootstrap CSS -->
          <title>Hello, world!</title>
          <link href="https://fonts.googleapis.com/css2?family=Bangers&display=swap" rel="stylesheet">
          <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300&display=swap" rel="stylesheet">
      </head>
      </head>
      <body>
          <div style="border-radius: 65px;
            border: 3px solid rgba(243,161,163,1);;
            width: 600px;
            background-color: rgba(255,249,248,1);
            height: 100%;font-family:'Poppins', sans-serif;;">
            <div style="float: left;
                margin-left: 20px;
                margin-right: 2px;
                margin-top: 30px;">
                <img class="aligncenter size-full wp-image-19768" src="http://bakeapp.naresh@thorsignia.online/static/assets/images/LogoHomeBakers.png" alt="one" width="105" height="105" />
            </div>
            <div style="margin: 55px;
                padding-left: 13%;
                width: auto;">
                <img src="http://bakeapp.naresh@thorsignia.online/static/assets/images/Capture-removebg-preview.png" width="80%">
            </div>
            <div style="margin-top: 10px ; font-size: 18px; margin-left: 35px;">
                <p style="font-size: 22px;letter-spacing: 1px;font-weight: 500;">Online Platform for Homebakers</p>
            </div>
            <div style="padding-left: 40px;margin-top: 10px;  font-size: 15px;">
                <p style="font-size: 15px;font-weight: 600;">Conform and Convenience</p>
                <p style="padding-left: 10px;">- A Dedicated Web and App (iOS and Android) platform only for Home<br> Bakers<br>
                    - Better visibility and wide audience coverage compared to the Other social<br>media platforms
                    <br>- No Need to invest in logistics or office set up - we will take care of those <br>tasks -Customer service, 
                  feedbacks, follow ups, payment collection, delivery<br> etc.<br>
                  - Easy to manage and editable menu options and price of your food items<br>
                  - Flexibility and convenience of scheduling orders as per your desired<br> timelines<br>
                  - Different Payments options (COD / CC / DC / Net Banking etc.)<br>
                  - Will assist you in getting your compliances<br>
                  - Daily, weekly reports of sales, collections etc. and daily settlement with<br> bakers
                </p>
            </div>
            <div style="margin-left: 40px; font-size: 15px;">
                <p style="font-size: 15px;font-weight: 600;">Your Online Blogs</p>
                <p style="padding-left: 10px;">- You will have your own business profile page where you can showcase 
                    your<br> amazing work,share your cooking videos (in a later stage), share
                    your<br> achievement with the customers <br>
                    - Easy to manage customers testimonials.
                </p>
            </div>
            <div style="margin-left: 40px;font-size: 15px;" >
                <p style="font-size: 15px;font-weight: 600;">Delivery</p>
                <p style="padding-left: 10px;">- No more delivery Hassle, we got this covered.
                    <br>- Easy to track your delivery.
                    <br>- Delivering in Delhi and NCR only for Gurgaon bakers (first phase.)
                </p>
            </div>
          </div>
      </body>
    </html>
    ''', subtype='html')
    s = smtplib.SMTP('naresh@thorsignia.online') 
    s.starttls()
    s.login("no-reply@petapp.naresh@thorsignia.online","Naresh@9902")
    s.sendmail("no-reply@petapp.naresh@thorsignia.online", receiver_mail, msg.as_string())
    return True




from django.http import JsonResponse
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from requests.exceptions import HTTPError
 
# from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
from . import serializers
 
class SocialLoginView(generics.GenericAPIView):
    """Log in using facebook"""
    serializer_class = serializers.SocialSerializer
    permission_classes = [permissions.AllowAny]
 
    def post(self, request):
        """Authenticate user through the provider and access_token"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.data.get('provider', None)
        strategy = load_strategy(request)
 
        try:
            backend = load_backend(strategy=strategy, name=provider,
            redirect_uri=None)
 
        except MissingBackend:
            return Response({'error': 'Please provide a valid provider'},
            status=status.HTTP_400_BAD_REQUEST)
        try:
            if isinstance(backend, BaseOAuth2):
                access_token = serializer.data.get('access_token')
            user = backend.do_auth(access_token)
        except HTTPError as error:
            return Response({
                "error": {
                    "access_token": "Invalid token",
                    "details": str(error)
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        except AuthTokenError as error:
            return Response({
                "error": "Invalid credentials",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)
 
        try:
            authenticated_user = backend.do_auth(access_token, user=user)
        
        except HTTPError as error:
            return Response({
                "error":"invalid token",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except AuthForbidden as error:
            return Response({
                "error":"invalid token",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)
 
        if authenticated_user and authenticated_user.is_active:
            #generate JWT token
            login(request, authenticated_user)
            data={
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )}
            #customize the response to your needs
            response = {
                "email": authenticated_user.email,
                "username": authenticated_user.username,
                "token": data.get('token')
            }
            return Response(status=status.HTTP_200_OK, data=response)    



from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
import uuid
 
class RegistrationappAPIView(generics.GenericAPIView): 
    serializer_class=  RegistrationSerializer 
    def post(self, requset):
        serializer=self.get_serializer(data=requset.data)
        # serializer.is_valid(raise_exception=True)  
        # serializer.save()

        if(serializer.is_valid()):
            serializer.save()
            return Response({
                
                "RequestId":str(uuid.uuid4()),
                "message":"user created Sucessfully",
                "User":serializer.data}, status=status.HTTP_201_CREATED
                )    
        return Response({"Errors":serializer.error}, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login

class loginview(views.APIView):
#    permission_classes = [
#        permissions.AllowAny  # Anyone can Login
#    ]

   def post(self,request):

      email_address = request.data.get('email')
      user_request = get_object_or_404(
        Users,
        email=email_address,
      )
      username = user_request.username

      password = request.data.get("password")

      user = authenticate(username=username, password=password)
      id_u = user.id
      if not user:
          return Response({"error": "Login failed"}, 
                               status=status.HTTP_401_UNAUTHORIZED)

      token, _ = Token.objects.get_or_create(user=user)
      return Response({"token": token.key,'id':id_u})

      


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })      





from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
# from jwt import PyJWKClient
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import views
class RegistersView(generics.GenericAPIView):
    serializer_class=RegisterSerializer
    def post(self,request):
        user = request.data
        serializer= self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data=serializer.data
        user=Users.objects.get(email=user_data['email'])

        token= RefreshToken.for_user(user).access_token
        relativeLink=reverse('email-verify')
        current_site= get_current_site(request).domain

        
        absurl='http://'+current_site+relativeLink+"?token="+str(token)
        email_body='Hi petapp' +user.username+'use link below to verify your email \n'+absurl
        data={'email_body':email_body,'to_email':user.email, 'email_subject': 'verify your email'}
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)  

from petishh.settings import SECRET_KEY

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"], options={"verify_signature": False})
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)         



class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
class UsercountView(APIView):
    renderer_class=[JSONRenderer]
    def get(self, request):
        user_count=User.objects.filter(is_active=True).count() 
        return Response(status=status.HTTP_200_OK, data={'user_count': user_count})

