from fcm_django.models import FCMDevice

from django.utils.crypto import get_random_string
from rest_framework import generics, permissions, status, views, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from user.serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# from sellerMenu.models import *
import django.db.models
from django.core.mail import send_mail
import random
from django.utils import timezone
import os
class FcmDeviceView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    #### Get All Profile Information
    def get(self, request, format=None):
        user = request.user
        user_id = user.id
        response_data = {}
        user= User.objects.filter(id=user_id, is_blocked=False, is_deleted=False)
        if user:
            rs = FCMDevice.objects.all()
            if rs:
                user_serialize = FireBaseDeviceAccess(rs, many=True)
                response_data['status'] = 1
                response_data['msg'] = 'Successfully get seller details'
                response_data['fcm_device'] = user_serialize.data
                http_status_code = 200
            else:
                response_data['status'] = 0
                response_data['msg'] = 'No data found'
                response_data['fcm_device'] = []
                http_status_code = 404
        else:
            response_data['status'] = 0
            response_data['msg'] = 'User Not Found'
            http_status_code = 404
        return Response(response_data, status=http_status_code)

    
    def post(self, request):
        user = request.user
        user_id = user.id
        requestdata = request.data
        response = {}
        print(requestdata)
        rs = User.objects.filter(id=user_id, is_blocked=False, is_deleted=False)
        if rs:
            check_device = FCMDevice.objects.filter(user_id=user_id).count()
            if check_device > 0:
                print('Updating ...')
                obj = FCMDevice.objects.filter(user_id=user_id).update(
                    registration_id =requestdata['registration_id'],
                    user_id = user_id,
                    type=requestdata['type']
                )
                response['status'] = 1
                response['msg'] = 'Updated'
                http_status_code = 200
            else:
                for i in rs:
                    username=i.username
                obj = FCMDevice.objects.create(
                    user_id=user_id,
                    name = username,
                    registration_id = requestdata['registration_id'],
                    type =requestdata['type'],
                    date_created=timezone.now(),
                )
                rs = FCMDevice.objects.filter(registration_id=requestdata['registration_id'])
                serializer = FireBaseDeviceAccess(rs, many=True)
                response['status'] = 1
                response['msg'] = 'New Category Added'
                response['fcm_device'] = serializer.data
                http_status_code = 201
        return Response(response, status=http_status_code)



class FcmSaveNotification(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        user = request.user
        user_id = user.id
        response_data = {}
        user= User.objects.filter(id=user_id, is_blocked=False, is_deleted=False)
        if user:
            rs = Notification.objects.filter(user_id=user_id).order_by('-id')[:4]
            if rs:
                user_serialize = NotificationMsg(rs, many=True)
                response_data['status'] = 1
                response_data['msg'] = 'Successfully get user notification'
                response_data['notifications'] = user_serialize.data
                http_status_code = 200
            else:
                response_data['status'] = 0
                response_data['msg'] = 'No Notification'
                response_data['notifications'] = []
                http_status_code = 202
        else:
            response_data['status'] = 0
            response_data['msg'] = 'User Not Found'
            http_status_code = 404
        return Response(response_data, status=http_status_code)

    
    def post(self, request):
        user = request.user
        user_id = user.id
        requestdata = request.data
        response_data = {}
        print(requestdata)
        rs = User.objects.filter(id=user_id, is_blocked=False, is_deleted=False)
        if rs:
            obj = Notification.objects.create(
                user_id=requestdata['vendor_id'],
                message = requestdata['message'],
                title= requestdata['title'],
                datamsg= requestdata['datamsg'],
                created_date=timezone.now(),
            )
            device = FCMDevice.objects.filter(user_id=requestdata['vendor_id']).first()
            device.send_message(title=requestdata['title'], body=requestdata['message'], data={"test": requestdata['datamsg']})
            response_data['status'] = 1
            response_data['msg'] = 'Sent'
            http_status_code = 200
        else:
            response_data['status'] = 0
            response_data['msg'] = 'User Not Found'
            http_status_code = 404
        return Response(response_data, status=http_status_code)