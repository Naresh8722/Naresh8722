from django.utils.crypto import get_random_string
from rest_framework import generics, permissions
from rest_framework.response import Response
from user.serializers import *
from rest_framework_simplejwt import authentication
from django.core.mail import send_mail
import random
from django.utils import timezone
import os
from rest_framework import viewsets
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from base64 import urlsafe_b64decode
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import smart_str, smart_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from user.utils import Util

class CustomerProfileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication,)
    queryset=User.objects.all()
    serializer_class=CustomerProfileSerializer
    # Get All Profile Information
    def get(self, request, format=None):
        user = request.user
        user_id = user.id
        response_data = {}
        profile_image_name = ''
        rs = User.objects.filter(
            id=user_id, is_active=True, is_blocked=False, is_deleted=False)
        if rs:
            user_serialize = CustomerProfileSerializer(rs, many=True)
            for details in user_serialize.data:
                profile_image_name = details['profile_image']
                if profile_image_name is not None:
                    if os.path.exists('media/profile_image/' + profile_image_name):
                        base64_image = encode_image_base64(
                            settings.MEDIA_ROOT + '/profile_image/' + profile_image_name)
                        details['profile_image'] = base64_image
            response_data['status'] = 1
            response_data['msg'] = 'Successfully get  details'
            response_data['profile_details'] = user_serialize.data
            http_status_code = 200
        else:
            response_data['status'] = 0
            response_data['msg'] = 'No data found'
            response_data['profile_details'] = []
            http_status_code = 404
        return Response(response_data, status=http_status_code)

# For edit profile
    def post(self, request, format=None):
        response_data = {}
        user = request.user
        user_id = user.id
        rs = User.objects.filter(
            id=user_id, is_active=True, is_blocked=False, is_deleted=False).first()
        if rs:
            obj = User.objects.filter(id=user_id).update(
                first_name=request.data['first_name'],
                last_name=request.data['last_name'],
                profile_image=request.data['profile_image'],
                home_address=request.data['home_address'],
                address=request.data['address'],
            )
            response_data['status'] = 1
            response_data['massage'] = "User update successfully"
            response_data['user_id'] = user_id
            return Response(response_data, status=200)
        else:
            response_data['status'] = 0
            response_data['massage'] = "User not found"
            response_data['user_id'] = user_id
            return Response(response_data, status=200)


# class RequestPasswordResetEmail(generics.GenericAPIView):
#     serializer_class = ResetPasswordEmailRequestSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         email = request.data['email']

#         if User.objects.filter(email=email).exists():
#             user = User.objects.get(email=email)
#             uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
#             token = PasswordResetTokenGenerator().make_token(user)
#             current_site = get_current_site(request=request).domain
#             relativeLink = reverse('password-reset-complete',kwargs={'uidb64':uidb64,'token':token})
#             absurl = 'http://'+current_site+ relativeLink
#             email_body = "Hello, \n Use this below link to reset your Password\n"+ absurl
#             data = {'email_body':email_body,"to_email":user.email, "email_subject":"Reset Your Password"}
#             Util.send_email(data)
#         return Response({'Success':"We have sent you a link to reset your password"})

# class PasswordTokenCheckAPI(generics.GenericAPIView):
#     def get(self,request, uidb64,token):
#         try:
#             id =  smart_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(id=id)

#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 return Response({'error':"Token is not valid, please request a new one "})
#             return Response({'Success':True,'message':'Credentials Valid','uidb64':uidb64,'token':token})
#         except:
#             return Response({'error':"Token is not valid, please request a new one "})


# class SetNewPasswordAPIView(generics.GenericAPIView):
#     serializer_class = SetNewPasswordSerializer

#     def patch(self, request, uidb64, token):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response({'Success':True, 'message':'Password reset successful'})


# class SetNewPasswordAPIView(generics.GenericAPIView):
#     serializer_class = SetNewPasswordSerializer

#     def post(self, request, uidb64, token):
#         try:
#             id =force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(id=id)
#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 raise AuthenticationFailed("The reset link is invalid",401)
#             password = request.data['password']
#             user.set_password(password)
#             user.save()
#         except Exception as e:
#             return Response({'msg':"Error"})
        
#         return Response({'Success':True, 'message':'Password reset successful'})
        

def encode_image_base64(full_path):
    image = ''
    if full_path != "":
        with open(full_path, 'rb') as imgFile:
            image = base64.b64encode(imgFile.read())
    return image
