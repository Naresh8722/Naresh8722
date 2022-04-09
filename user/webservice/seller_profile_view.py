from django.db.models import query
from django.http.response import JsonResponse
from django.utils.crypto import get_random_string
from rest_framework import generics, permissions, status, views, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from user.serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from sellerMenu.models import *
from payments.models import *
import django.db.models
from django.core.mail import send_mail
import random
from django.utils import timezone
import os
import googlemaps

from django.shortcuts import render
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib,ssl
from email.message import EmailMessage
import os
from io import BytesIO
from PIL import Image
from django.core.files import File


def compress(image):
    img = Image.open(image)
    img_io = BytesIO() 
    img.thumbnail((500, 500))
    img.save(img_io, 'JPEG', quality=70) 
    new_image = File(img_io, name=image.name)
    return new_image


def encode_image_base64(full_path):
    image = ''
    if full_path != "":
        with open(full_path, 'rb') as imgFile:
            image = base64.b64encode(imgFile.read())
    return image


def imgcomp(image):
    newimg = ""
    image = Image.open(image)
    image.save(newimg, format="JPEG", quality=70)
    return newimg
    

class AdminSellerProfileView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    #### Get All Profile Information
    def post(self, request, format=None):
        user = request.user
        user_id = user.id
        requestdata = request.data
        response_data = {}
        profile_image_name = ''
        shop_image_name = ''
        aadhaar_front_image_name = ''
        aadhaar_back_image_name = ''
        owner_image_name = ''
        gstin_image_name = ''
        fssal_image_name = ''
        pancard_image_name =''
        image1_name =""
        image2_name =""
        image3_name =""
        image4_name =""
        image5_name =""
        image6_name =""
        image7_name =""
        image8_name =""
        image9_name =""
        image10_name =""
        rs = User.objects.filter(id=user_id, is_superuser=True, is_active=True, is_blocked=False, is_deleted=False)
        if rs:
            vrs = User.objects.filter(id=requestdata['vendor_id'], is_active=True, is_blocked=False, is_deleted=False)
            user_serialize = SellerProfileSerializer(vrs, many=True)
            for details in user_serialize.data:
                profile_image_name = details['profile_image']
                shop_image_name = details['shop_image']
                aadhaar_front_image_name = details['aadhaar_front_image']
                aadhaar_back_image_name = details['aadhaar_back_image']
                owner_image_name = details['owner_image']
                gstin_image_name = details['gstin_image']
                fssai_image_name = details['fssai_image']
                pancard_image_name = details['pancard_image']
                if profile_image_name is not None:
                    if os.path.exists('media/profile_image/' + profile_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/profile_image/' + profile_image_name)
                        details['profile_image'] = base64_image
                if shop_image_name is not None:
                    if os.path.exists('media/shop_image/' + shop_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/shop_image/' + shop_image_name)
                        details['shop_image'] = base64_image
                if owner_image_name is not None:
                    if os.path.exists('media/owner_image/' + owner_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/owner_image/' + owner_image_name)
                        details['owner_image'] = base64_image
                if aadhaar_front_image_name is not None:
                    if os.path.exists('media/aadhaar_front_image/' + aadhaar_front_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/aadhaar_front_image/' + aadhaar_front_image_name)
                        details['aadhaar_front_image'] = base64_image
                if aadhaar_back_image_name is not None:
                    if os.path.exists('media/aadhaar_back_image/' + aadhaar_back_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/aadhaar_back_image/' + aadhaar_back_image_name)
                        details['aadhaar_back_image'] = base64_image
                if gstin_image_name is not None:
                    if os.path.exists('media/gstin_image/' + gstin_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/gstin_image/' + gstin_image_name)
                        details['gstin_image'] = base64_image
                if fssai_image_name is not None:
                    if os.path.exists('media/fssai_image/' + fssai_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/fssai_image/' + fssai_image_name)
                        details['fssai_image'] = base64_image
                if pancard_image_name is not None:
                    if os.path.exists('media/pancard_image/' + pancard_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/pancard_image/' + pancard_image_name)
                        details['pancard_image'] = base64_image
            gallery = Profileinfo.objects.filter(user_id=requestdata['vendor_id'])
            if gallery:
                category_serialize = SellerProfileInfoListSerializer(gallery, many=True)
                for details in category_serialize.data:
                    image1_name= details['image1']
                    image2_name= details['image2']
                    image3_name= details['image3']
                    image4_name= details['image4']
                    image5_name= details['image5']
                    image6_name= details['image6']
                    image7_name= details['image7']
                    image8_name= details['image8']
                    image9_name= details['image9']
                    image10_name= details['image10']
                    if image1_name is not None:
                        if os.path.exists('media/profile_gallery/' + image1_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image1_name)
                            details['image1'] = base64_image
                    if image2_name is not None:
                        if os.path.exists('media/profile_gallery/' + image2_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image2_name)
                            details['image2'] = base64_image
                    if image3_name is not None:
                        if os.path.exists('media/profile_gallery/' + image3_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image3_name)
                            details['image3'] = base64_image
                    if image4_name is not None:
                        if os.path.exists('media/profile_gallery/' + image4_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image4_name)
                            details['image4'] = base64_image
                    if image5_name is not None:
                        if os.path.exists('media/profile_gallery/' + image5_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image5_name)
                            details['image5'] = base64_image
                    if image6_name is not None:
                        if os.path.exists('media/profile_gallery/' + image6_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image6_name)
                            details['image6'] = base64_image
                    if image7_name is not None:
                        if os.path.exists('media/profile_gallery/' + image7_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image7_name)
                            details['image7'] = base64_image
                    if image8_name is not None:
                        if os.path.exists('media/profile_gallery/' + image8_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image8_name)
                            details['image8'] = base64_image
                    if image9_name is not None:
                        if os.path.exists('media/profile_gallery/' + image9_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image9_name)
                            details['image9'] = base64_image

                    if image10_name is not None:
                        if os.path.exists('media/profile_gallery/' + image10_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image10_name)
                            details['image10'] = base64_image
                response_data['gallery_details'] = category_serialize.data
                response_data['status'] = 1
                response_data['msg'] = 'Successfully get seller details'
                response_data['profile_details'] = user_serialize.data
                http_status_code = 200
            else:
                response_data['gallery_details'] =[]
                response_data['status'] = 1
                response_data['msg'] = 'Successfully get seller details'
                response_data['profile_details'] = user_serialize.data
                http_status_code = 200
        else:
            response_data['status'] = 0
            response_data['msg'] = 'No data found'
            response_data['profile_details'] = []
            response_data['gallery_details'] =[]
            http_status_code = 404
        return Response(response_data, status=http_status_code)


class CustomerSellerProfileView(generics.ListAPIView):
    queryset=''
    serializer_class=SellerProfileSerializer
    #### Get All Profile Information
    def post(self, request, format=None):
        user = request.user
        #user_id = user.id
        response_data = {}
        profile_image_name = ''
        shop_image_name = ''
        aadhaar_front_image_name = ''
        aadhaar_back_image_name = ''
        owner_image_name = ''
        gstin_image_name = ''
        # fssal_image_name = ''
        pancard_image_name =''
        image1_name =""
        image2_name =""
        image3_name =""
        image4_name =""
        image5_name =""
        image6_name =""
        image7_name =""
        image8_name =""
        image9_name =""
        image10_name =""
        user_id = request.data['id']
        rs = User.objects.filter(id=user_id, is_active=True, is_blocked=False, is_deleted=False)
        if rs:  
            user_serialize = SellerProfileSerializer(rs, many=True)
            for details in user_serialize.data:
                profile_image_name = details['profile_image']
                shop_image_name = details['shop_image']
                aadhaar_front_image_name = details['aadhaar_front_image']
                aadhaar_back_image_name = details['aadhaar_back_image']
                owner_image_name = details['owner_image']
                gstin_image_name = details['gstin_image']
                fssai_image_name = details['fssai_image']
                pancard_image_name = details['pancard_image']
                if profile_image_name is not None:
                    if os.path.exists('media/profile_image/' + profile_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/profile_image/' + profile_image_name)
                        details['profile_image'] = base64_image
                if shop_image_name is not None:
                    if os.path.exists('media/shop_image/' + shop_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/shop_image/' + shop_image_name)
                        details['shop_image'] = base64_image
                if owner_image_name is not None:
                    if os.path.exists('media/owner_image/' + owner_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/owner_image/' + owner_image_name)
                        details['owner_image'] = base64_image
                if aadhaar_front_image_name is not None:
                    if os.path.exists('media/aadhaar_front_image/' + aadhaar_front_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/aadhaar_front_image/' + aadhaar_front_image_name)
                        details['aadhaar_front_image'] = base64_image
                if aadhaar_back_image_name is not None:
                    if os.path.exists('media/aadhaar_back_image/' + aadhaar_back_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/aadhaar_back_image/' + aadhaar_back_image_name)
                        details['aadhaar_back_image'] = base64_image
                if gstin_image_name is not None:
                    if os.path.exists('media/gstin_image/' + gstin_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/gstin_image/' + gstin_image_name)
                        details['gstin_image'] = base64_image
                if fssai_image_name is not None:
                    if os.path.exists('media/fssai_image/' + fssai_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/fssai_image/' + fssai_image_name)
                        details['fssai_image'] = base64_image
                if pancard_image_name is not None:
                    if os.path.exists('media/pancard_image/' + pancard_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/pancard_image/' + pancard_image_name)
                        details['pancard_image'] = base64_image
            gallery = Profileinfo.objects.filter(user_id=user_id)
            if gallery:
                category_serialize = SellerProfileInfoListSerializer(gallery, many=True)
                for details in category_serialize.data:
                    image1_name= details['image1']
                    image2_name= details['image2']
                    image3_name= details['image3']
                    image4_name= details['image4']
                    image5_name= details['image5']
                    image6_name= details['image6']
                    image7_name= details['image7']
                    image8_name= details['image8']
                    image9_name= details['image9']
                    image10_name= details['image10']
                    if image1_name is not None:
                        if os.path.exists('media/profile_gallery/' + image1_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image1_name)
                            details['image1'] = base64_image
                    if image2_name is not None:
                        if os.path.exists('media/profile_gallery/' + image2_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image2_name)
                            details['image2'] = base64_image
                    if image3_name is not None:
                        if os.path.exists('media/profile_gallery/' + image3_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image3_name)
                            details['image3'] = base64_image
                    if image4_name is not None:
                        if os.path.exists('media/profile_gallery/' + image4_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image4_name)
                            details['image4'] = base64_image
                    if image5_name is not None:
                        if os.path.exists('media/profile_gallery/' + image5_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image5_name)
                            details['image5'] = base64_image
                    if image6_name is not None:
                        if os.path.exists('media/profile_gallery/' + image6_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image6_name)
                            details['image6'] = base64_image
                    if image7_name is not None:
                        if os.path.exists('media/profile_gallery/' + image7_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image7_name)
                            details['image7'] = base64_image
                    if image8_name is not None:
                        if os.path.exists('media/profile_gallery/' + image8_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image8_name)
                            details['image8'] = base64_image
                    if image9_name is not None:
                        if os.path.exists('media/profile_gallery/' + image9_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image9_name)
                            details['image9'] = base64_image

                    if image10_name is not None:
                        if os.path.exists('media/profile_gallery/' + image10_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image10_name)
                            details['image10'] = base64_image
                response_data['gallery_details'] = category_serialize.data
                response_data['status'] = 1
                response_data['msg'] = 'Successfully get seller details'
                response_data['profile_details'] = user_serialize.data
                http_status_code = 200
            else:
                response_data['gallery_details'] =[]
                response_data['status'] = 1
                response_data['msg'] = 'Successfully get seller details'
                response_data['profile_details'] = user_serialize.data
                http_status_code = 200
        else:
            response_data['status'] = 0
            response_data['msg'] = 'No data found'
            response_data['profile_details'] = []
            response_data['gallery_details'] =[]
            http_status_code = 404
        return Response(response_data, status=http_status_code)


class SellerProfileHeaderView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    #### Get All Profile Information
    def get(self, request, format=None):
        user = request.user
        user_id = user.id
        response_data = {}
        profile_image_name = ''
        rs = User.objects.filter(id=user_id, is_active=True, is_blocked=False, is_deleted=False)
        if rs:
            user_serialize = SellerProfileSerializer(rs, many=True)
            for details in user_serialize.data:
                profile_image_name = details['profile_image']
                if profile_image_name is not None:
                    if os.path.exists('media/profile_image/' + profile_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/profile_image/' + profile_image_name)
                        details['profile_image'] = base64_image
               
                response_data['status'] = 1
                response_data['msg'] = 'Successfully get seller details'
                response_data['name'] = user_serialize.data[0]['first_name']
                response_data['status flag'] = user_serialize.data[0]['status']
                response_data['profile_image'] = user_serialize.data[0]['profile_image']
                http_status_code = 200
            
        else:
            response_data['status'] = 0
            response_data['msg'] = 'No data found'
            response_data['profile_image'] = []
            response_data['name'] = []
            response_data['status flag'] = []
            http_status_code = 404
        
        return Response(response_data, status=http_status_code)





class SellerProfileView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    #### Get All Profile Information
    def get(self, request, format=None):
        user = request.user
        user_id = user.id
        response_data = {}
        profile_image_name = ''
        shop_image_name = ''
        aadhaar_front_image_name = ''
        aadhaar_back_image_name = ''
        owner_image_name = ''
        gstin_image_name = ''
        fssal_image_name = ''
        pancard_image_name =''
        image1_name =""
        image2_name =""
        image3_name =""
        image4_name =""
        image5_name =""
        image6_name =""
        image7_name =""
        image8_name =""
        image9_name =""
        image10_name =""
        rs = User.objects.filter(id=user_id, is_active=True, is_blocked=False, is_deleted=False)
        if rs:
            user_serialize = SellerProfileSerializer(rs, many=True)
            for details in user_serialize.data:
                profile_image_name = details['profile_image']
                shop_image_name = details['shop_image']
                aadhaar_front_image_name = details['aadhaar_front_image']
                aadhaar_back_image_name = details['aadhaar_back_image']
                owner_image_name = details['owner_image']
                gstin_image_name = details['gstin_image']
                fssai_image_name = details['fssai_image']
                pancard_image_name = details['pancard_image']
                if profile_image_name is not None:
                    if os.path.exists('media/profile_image/' + profile_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/profile_image/' + profile_image_name)
                        details['profile_image'] = base64_image
                if shop_image_name is not None:
                    if os.path.exists('media/shop_image/' + shop_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/shop_image/' + shop_image_name)
                        details['shop_image'] = base64_image
                if owner_image_name is not None:
                    if os.path.exists('media/owner_image/' + owner_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/owner_image/' + owner_image_name)
                        details['owner_image'] = base64_image
                if aadhaar_front_image_name is not None:
                    if os.path.exists('media/aadhaar_front_image/' + aadhaar_front_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/aadhaar_front_image/' + aadhaar_front_image_name)
                        details['aadhaar_front_image'] = base64_image
                if aadhaar_back_image_name is not None:
                    if os.path.exists('media/aadhaar_back_image/' + aadhaar_back_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/aadhaar_back_image/' + aadhaar_back_image_name)
                        details['aadhaar_back_image'] = base64_image
                if gstin_image_name is not None:
                    if os.path.exists('media/gstin_image/' + gstin_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/gstin_image/' + gstin_image_name)
                        details['gstin_image'] = base64_image
                if fssai_image_name is not None:
                    if os.path.exists('media/fssai_image/' + fssai_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/fssai_image/' + fssai_image_name)
                        details['fssai_image'] = base64_image
                if pancard_image_name is not None:
                    if os.path.exists('media/pancard_image/' + pancard_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/pancard_image/' + pancard_image_name)
                        details['pancard_image'] = base64_image
            gallery = Profileinfo.objects.filter(user_id=user_id)
            if gallery:
                category_serialize = SellerProfileInfoListSerializer(gallery, many=True)
                for details in category_serialize.data:
                    image1_name= details['image1']
                    image2_name= details['image2']
                    image3_name= details['image3']
                    image4_name= details['image4']
                    image5_name= details['image5']
                    image6_name= details['image6']
                    image7_name= details['image7']
                    image8_name= details['image8']
                    image9_name= details['image9']
                    image10_name= details['image10']
                    if image1_name is not None:
                        if os.path.exists('media/profile_gallery/' + image1_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image1_name)
                            details['image1'] = base64_image
                    if image2_name is not None:
                        if os.path.exists('media/profile_gallery/' + image2_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image2_name)
                            details['image2'] = base64_image
                    if image3_name is not None:
                        if os.path.exists('media/profile_gallery/' + image3_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image3_name)
                            details['image3'] = base64_image
                    if image4_name is not None:
                        if os.path.exists('media/profile_gallery/' + image4_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image4_name)
                            details['image4'] = base64_image
                    if image5_name is not None:
                        if os.path.exists('media/profile_gallery/' + image5_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image5_name)
                            details['image5'] = base64_image
                    if image6_name is not None:
                        if os.path.exists('media/profile_gallery/' + image6_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image6_name)
                            details['image6'] = base64_image
                    if image7_name is not None:
                        if os.path.exists('media/profile_gallery/' + image7_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image7_name)
                            details['image7'] = base64_image
                    if image8_name is not None:
                        if os.path.exists('media/profile_gallery/' + image8_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image8_name)
                            details['image8'] = base64_image
                    if image9_name is not None:
                        if os.path.exists('media/profile_gallery/' + image9_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image9_name)
                            details['image9'] = base64_image

                    if image10_name is not None:
                        if os.path.exists('media/profile_gallery/' + image10_name):
                            base64_image = encode_image_base64(
                                settings.MEDIA_ROOT + '/profile_gallery/' + image10_name)
                            details['image10'] = base64_image
                response_data['gallery_details'] = category_serialize.data
                response_data['status'] = 1
                response_data['msg'] = 'Successfully get seller details'
                response_data['profile_details'] = user_serialize.data
                http_status_code = 200
            else:
                response_data['gallery_details'] =[]
                response_data['status'] = 1
                response_data['msg'] = 'Successfully get seller details'
                response_data['profile_details'] = user_serialize.data
                http_status_code = 200
        else:
            response_data['status'] = 0
            response_data['msg'] = 'No data found'
            response_data['profile_details'] = []
            response_data['gallery_details'] =[]
            http_status_code = 404
        return Response(response_data, status=http_status_code)

    def put(self, request, format=None):
        response_data = {}
        user = request.user
        user_id = user.id
        requestdata = request.data
        rs = User.objects.filter(id=user_id, is_active=True, is_blocked=False, is_deleted=False).first()
        if rs:
            obj = User.objects.filter(id=user_id).update(
                address = requestdata['address'],
                pin_code=requestdata['pin_code'],
                owner_name=requestdata['owner_name'],
                shop_name=requestdata['shop_name'],
                dateofbirth=requestdata['dateofbirth'],
                adhaarcard=requestdata['adhaarcard'],
                pancard=requestdata['pancard'],
                pancardtype=requestdata['pancardtype'],
                shop_city = requestdata['shop_city'],
                shop_landmark =requestdata['shop_landmark'],
                modified_date=timezone.now(),
                floor_no = requestdata['floor_no'],
                mall_name = requestdata['mall_name'],
                shop_area = requestdata['shop_area'],
                state= requestdata['state'],
                latitude= requestdata['latitude'],
                longitude = requestdata['longitude']
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



class SellerGstUpdate(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    
    def put(self, request, format=None):
        response_data = {}
        user = request.user
        user_id = user.id
        requestdata = request.data
        rs = User.objects.filter(id=user_id, is_active=True, is_blocked=False, is_deleted=False).first()
        if rs:
            obj = User.objects.filter(id=user_id).update(
                gstin_number=requestdata['gstin_number'],
                registration_date=requestdata['registration_date'],
                gst_state=requestdata['gst_state'],
            )
            response_data['status'] = 1
            response_data['massage'] = "Saved Successfully"
            response_data['user_id'] = user_id
            return Response(response_data, status=200)
        else:
            response_data['status'] = 0
            response_data['massage'] = "User not found"
            response_data['user_id'] = user_id
            return Response(response_data, status=200)


# class SellerFssaiUpdate(generics.ListAPIView):
#     permission_classes = (IsAuthenticated,)
    
#     def put(self, request, format=None):
#         response_data = {}
#         user = request.user
#         user_id = user.id
#         requestdata = request.data
#         rs = User.objects.filter(id=user_id, is_active=True, is_blocked=False, is_deleted=False).first()
#         if rs:
#             obj = User.objects.filter(id=user_id).update(
#                 fssai_number=requestdata['fssai_number'],
#                 fssai_reg_name=requestdata['fssai_reg_name'],
#                 fssai_exp_date=requestdata['fssai_exp_date'],
#                 fssai_address = requestdata['fssai_address']
#             )
#             response_data['status'] = 1
#             response_data['massage'] = "Saved Successfully"
#             response_data['user_id'] = user_id
#             return Response(response_data, status=200)
#         else:
#             response_data['status'] = 0
#             response_data['massage'] = "User not found"
#             response_data['user_id'] = user_id
#             return Response(response_data, status=200)

class RegistrationSubmit(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    
    def put(self, request, format=None):
        response_data = {}
        user = request.user
        user_id = user.id
        requestdata = request.data
        rs = User.objects.filter(id=user_id, is_active=True, is_blocked=False, is_deleted=False).first()
        if rs:
            obj = User.objects.filter(id=user_id).update(
                is_submitted=requestdata['is_submitted']
            )
            response_data['status'] = 1
            response_data['massage'] = "Saved Successfully"
            response_data['user_id'] = user_id
            return Response(response_data, status=200)
        else:
            response_data['status'] = 0
            response_data['massage'] = "User not found"
            response_data['user_id'] = user_id
            return Response(response_data, status=200)


class SellerProfileUpdateView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        user = request.user
        user_id = user.id
        response_data = {}
        profile_image_name = ''
        rs = User.objects.filter(id=user_id, is_active=True, is_blocked=False, is_deleted=False)
        if rs:
            user_serialize = SellerProfileSerializer(rs, many=True)
            for details in user_serialize.data:
                profile_image_name = details['profile_image']
            if profile_image_name is not None:
                    if os.path.exists('media/profile_image/' + profile_image_name):
                        base64_image = encode_image_base64(settings.MEDIA_ROOT + '/profile_image/' + profile_image_name)
                        details['profile_image'] = base64_image
            response_data['status'] = 1
            response_data['msg'] = 'Successfully get seller details'
            response_data['profile_details'] = user_serialize.data
            http_status_code = 200
        else:
            response_data['status'] = 0
            response_data['msg'] = 'No data found'
            response_data['profile_details'] = []
            http_status_code = 404
        return Response(response_data, status=http_status_code)

    def put(self, request):
        user = request.user
        user_id = user.id
        response_data = {}
        rs = User.objects.filter(id=user_id, is_active=True, is_blocked=False, is_deleted=False)
        if rs:
            updateData= User.objects.filter(id=user_id).update(first_name=request.data['first_name'],last_name=request.data['last_name'],home_address=request.data['home_address'])
            response_data['status'] = 1
            response_data['msg'] = 'Successfully update Profile'
            http_status_code = 200
        else:
            response_data['status'] = 0
            response_data['msg'] = 'No User found'
            response_data['profile_details'] = []
            http_status_code = 404
        return Response(response_data, status=http_status_code)





class FileUploadView(mixins.CreateModelMixin, generics.ListAPIView):
    permission_classes = (IsAuthenticated,)


    def delete(self, request, *args, **kwargs):
        
        user = request.user
        user_id = user.id
        up_dir = request.data['up_dir']
        file_name_is = request.data['file_name']

        if up_dir == 'profile_gallery':
            image = request.data['image']
            update_data = {image:''}

            obj = Profileinfo.objects.filter(user_id = user_id).update(
                        **update_data
                    )
            
        elif up_dir == 'profile_image':

            obj = User.objects.filter(id=user_id).update(
                    profile_image=''
                )

        elif up_dir == 'shop_image':
            obj = User.objects.filter(id=user_id).update(
                    shop_image = ''
                )
            
        elif up_dir == 'owner_image':
            obj = User.objects.filter(id=user_id).update(
                    owner_image = ''
                )

        elif up_dir == 'aadhaar_back_image':
            obj = User.objects.filter(id=user_id).update(
                aadhaar_back_image = ''
            )
            
        elif up_dir == 'aadhaar_front_image':
            
            
            obj = User.objects.filter(id=user_id).update(
                aadhaar_front_image = ''
            )
            
        elif up_dir == 'gstin_image':
            obj = User.objects.filter(id=user_id).update(
                gstin_image =''
            )
            
        elif up_dir == 'fssai_image':
            obj = User.objects.filter(id=user_id).update(
                fssai_image =''
            )
            
        elif up_dir == 'category_image':
            obj = SellerCategory.objects.filter(id=user_id).update(
                category_image =''
            )
            
        elif up_dir == 'passbook_image':

            obj = VendorAddBankAccount.objects.filter(user_id=user_id).update(
                account_image = ''
            )
 
        elif up_dir == 'item_image':

            image = request.data['image']
            update_data = {image:''}
            
            obj = SellerItem.objects.filter(id=request.data['item_id']).update(
                **update_data
            )
            
        elif up_dir == 'banner_image':
            obj = Banner.objects.filter(user_id=user_id).update(
                banner_image = ''
            )
        
            
        elif up_dir == 'pancard_image':
            obj = User.objects.filter(id=user_id).update(
                pancard_image = ''
            )
            

        if os.path.exists('media/' + str(up_dir) + '/'):
            try:
                if file_name_is:
                    os.remove(os.path.join(settings.MEDIA_ROOT+ '/'+str(up_dir)+'/', file_name_is))

                    data = {
                            'status': 1, 
                            'deleted_file_name': file_name_is,
                            'message': 'File Deleted Successfully',
                        }
                    return Response(data)
                else:
                    data = {
                        'status': 0, 
                        'deleted_file_name': 'not found',
                        'message': 'File Not Found',
                    }
                    return Response(data)


            except:
                data = {
                    'status': 0,
                    'deleted_file_name': file_name_is,
                    'message': 'File extension error',
                }
            
            return Response(data)


    def post(self, request, *args, **kwargs):
        user = request.user
        user_id = user.id
        file1 = request.FILES['file']  ## Uploaded file
        file_type = request.data['file_type']  ## file Type i.e. image / doc / pdf   etc
        up_dir = request.data['up_dir']
        result_list = {}
        new_file_name = ''
        full_path_name = ''
        upload_status = False
        base64_image = ''
        if file_type is None:
            file_type = "img"
        if up_dir is None:
            up_dir = "images"
        image_name = file1.name
        name1 = get_random_string(length=8)
        ext = image_name.split('.')[-1]
        now = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
        uploaded_file_name = now + '.' + ext
        #####################################
        ## Check File Type (Only 'jpg', 'jpeg', 'gif', 'png','pdf' allowed)
        if ext in ['jpg', 'jpeg', 'gif', 'png']:
            if not os.path.exists('media/' + str(up_dir) + '/'):
                os.makedirs('media/' + str(up_dir) + '/')
            upload_to = 'media/' + str(up_dir) + '/%s' % (uploaded_file_name)
            fullpath = settings.BASE_DIR + '/media/' + str(up_dir)
            destination = open(upload_to, 'wb+')
            file1 = compress(file1)
            for chunk in file1.chunks():
                destination.write(chunk)
            destination.close()
            if up_dir == 'profile_gallery':
                image= request.data['image']
                if image == 'image1':
                    obj = Profileinfo.objects.filter(user_id=user_id).update(
                        image1 = uploaded_file_name
                    )
                elif image == 'image2':
                    obj = Profileinfo.objects.filter(user_id=user_id).update(
                        image2= uploaded_file_name
                    )
                elif image == 'image3':
                    obj = Profileinfo.objects.filter(user_id=user_id).update(
                        image3 = uploaded_file_name
                    )
                elif image == 'image4':
                    obj = Profileinfo.objects.filter(user_id=user_id).update(
                        image4 = uploaded_file_name
                    )
                elif image == 'image5':
                    obj = Profileinfo.objects.filter(user_id=user_id).update(
                        image5 = uploaded_file_name
                    )
                elif image == 'image6':
                    obj = Profileinfo.objects.filter(user_id=user_id).update(
                        image6 = uploaded_file_name
                    )
                elif image == 'image7':
                    obj = Profileinfo.objects.filter(user_id=user_id).update(
                        image7 = uploaded_file_name
                    )
                elif image == 'image8':
                    obj = Profileinfo.objects.filter(user_id=user_id).update(
                        image8 = uploaded_file_name
                    )
                elif image == 'image9':
                    obj = Profileinfo.objects.filter(user_id=user_id).update(
                        image9 = uploaded_file_name
                    )
                elif image == 'image10':
                    obj = Profileinfo.objects.filter(user_id=user_id).update(
                        image10 = uploaded_file_name
                    )
            elif up_dir == 'profile_image':
                obj = User.objects.filter(id=user_id).update(
                profile_image=uploaded_file_name
                )
            elif up_dir == 'shop_image':
                obj = User.objects.filter(id=user_id).update(
                shop_image =uploaded_file_name
                )
            elif up_dir == 'owner_image':
                obj = User.objects.filter(id=user_id).update(
                owner_image =uploaded_file_name
                )
            elif up_dir == 'aadhaar_back_image':
                obj = User.objects.filter(id=user_id).update(
                aadhaar_back_image =uploaded_file_name
                )
            elif up_dir == 'aadhaar_front_image':
                obj = User.objects.filter(id=user_id).update(
                aadhaar_front_image =uploaded_file_name
                )
            elif up_dir == 'gstin_image':
                obj = User.objects.filter(id=user_id).update(
                gstin_image =uploaded_file_name
                )
            elif up_dir == 'fssai_image':
                obj = User.objects.filter(id=user_id).update(
                fssai_image =uploaded_file_name
                )
            elif up_dir == 'category_image':
                obj = SellerCategory.objects.filter(id=user_id).update(
                category_image =uploaded_file_name
                )
            elif up_dir == 'passbook_image':
                obj = VendorAddBankAccount.objects.filter(user_id=user_id).update(
                    account_image = uploaded_file_name
                )
            elif up_dir == 'item_image':

                image = request.data['image']
                
                if image == 'image1':
                    obj = SellerItem.objects.filter(id=request.data['item_id']).update(
                        item_image1=uploaded_file_name
                    )
                if image == 'image2':
                    obj = SellerItem.objects.filter(id=request.data['item_id']).update(
                        item_image2=uploaded_file_name
                    )
                if image == 'image3':
                    obj = SellerItem.objects.filter(id=request.data['item_id']).update(
                        item_image3=uploaded_file_name
                    )
            elif up_dir == 'banner_image':
                obj = Banner.objects.create(banner_image = uploaded_file_name, status=True)
                obj.save()
                
            elif up_dir == 'pancard_image':
                 obj = User.objects.filter(id=user_id).update(
                    pancard_image = uploaded_file_name
                )
            # elif up_dir == 'profile_gallery':
            #      obj = User.objects.filter(id=user_id).update(
            #         pancard_image = uploaded_file_name
            #     )
            elif up_dir == 'profile_gallery':
                image= request.data['image']
                if image == 'image1':
                    obj = Profileinfo.objects.filter(user_id=user_id).update(
                        image1 = uploaded_file_name
                    )
                elif image == 'image2':
                    obj = Profileinfo.objects.filter(user_id=user_id).update(
                        image2= uploaded_file_name
                    )
                elif image == 'image3':
                    obj = Profileinfo.objects.filter(user_id=user_id).update(
                        image3 = uploaded_file_name
                    )
                elif image == 'image4':
                    obj = Profileinfo.objects.filter(user_id=user_id).update(
                        image4 = uploaded_file_name
                    )
                elif image == 'image5':
                    obj = Profileinfo.objects.filter(user_id=user_id).update(
                        image5 = uploaded_file_name
                    )
                elif image == 'image6':
                    obj = Profileinfo.objects.filter(user_id=user_id).update(
                        image6 = uploaded_file_name
                    )
                elif image == 'image7':
                    obj = Profileinfo.objects.filter(user_id=user_id).update(
                        image7 = uploaded_file_name
                    )
                elif image == 'image8':
                    obj = Profileinfo.objects.filter(user_id=user_id).update(
                        image8 = uploaded_file_name
                    )
                elif image == 'image9':
                    obj = Profileinfo.objects.filter(user_id=user_id).update(
                        image9 = uploaded_file_name
                    )
                elif image == 'image10':
                    obj = Profileinfo.objects.filter(user_id=user_id).update(
                        image10 = uploaded_file_name
                    )
                
            if os.path.exists('media/' + str(up_dir) + '/'):
                try:
                    base64_image = encode_image_base64(settings.MEDIA_ROOT + '/'+str(up_dir)+'/' + uploaded_file_name)
                except:
                    base64_image = ""
            data = {
                'status': 1,
                'base64_image': base64_image,
                'uploaded_file_name': uploaded_file_name,
                'uploaded_file_url': fullpath,
                'message': 'Uploaded Successfully',
            }
        else:
            data = {
                'status': 0,
                'base64_image': base64_image,
                'uploaded_file_name': '',
                'uploaded_file_url': '',
                'message': 'File extension error',
            }
        
        return Response(data)


## BioPreview By Admin

class BioPreviewApprove(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        userid = user.id
        response = {}
        requestData = request.data
        adm = User.objects.filter(id = userid, is_superuser = True)
        if adm:
            rs =  Profileinfo.objects.filter(user_id=requestData['user_id'])
            serializer = SellerProfileInfoSerializer(rs, many=True)
            for item in serializer.data:
                comment = requestData['comment']
                item['comment'] = comment
            Profileinfo.objects.filter(user_id=requestData['user_id']).update(is_approved=True,comment = comment)

            response['status'] = '1'
            response['Message'] = 'Bio is approved by admin'
            response['data'] = serializer.data
            return Response(response, status=200)
        else:
            response['status'] = '0'
            response['Message'] = 'Bio is not approved by admin'
            response['data'] = serializer.data
            return Response(response, status=200)


class BioPreviewDecline(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        user_id = user.id
        response = {}
        requestData = request.data
        adm = User.objects.filter(id = user_id, is_superuser = True)
        if adm:
            rs =  Profileinfo.objects.filter(user_id=requestData['user_id'])
            serializer = SellerProfileInfoSerializer(rs, many=True)
            for item in serializer.data:
                comment = requestData['comment']
                item['comment'] = comment
            Profileinfo.objects.filter(user_id=requestData['user_id']).update(is_approved=False,comment=comment)

            response['status'] = '1'
            response['Message'] = 'Bio is decline by admin'
            response['data'] = serializer.data
            return Response(response, status=200)
        else:
            response['status'] = '0'
            response['Message'] = 'Bio is not decline by admin'
            response['data'] = serializer.data
            return Response(response, status=200)




class AppRegSub(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        user_id = user.id
        response_data = {}
        rs = User.objects.filter(id=user_id, is_submitted=True)
        if rs:
            response_data['status'] = 1
            response_data['subStatus'] = True
            http_status_code = 200
        else:
            response_data['status'] = 1
            response_data['subStatus'] = False
            http_status_code = 200
        return Response(response_data, status=http_status_code)


class GetAddress(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
    
    def post(self, request, format=None):
        response_data = {}
        user = request.user
        user_id = user.id
        requestdata = request.data
        gmaps = googlemaps.Client(key='AIzaSyBlbSDe356E0-0k9nJpnTFotz_l9S1Kqqc')
        reverse_geocode_result = gmaps.reverse_geocode((requestdata["lati"], requestdata["longi"]))
        if reverse_geocode_result:
            data= reverse_geocode_result[1]["address_components"]
            for i in range(len(data)):
                if data[i]["types"][0]=="political":
                    response_data["area"] = data[i]["long_name"]
                if data[i]["types"][0]=="route":
                    response_data["address"] = data[i]["long_name"]
                if data[i]["types"][0]=="locality":
                    response_data["city"] = data[i]["long_name"]
                if data[i]["types"][0]=="administrative_area_level_1":
                    response_data["state"] = data[i]["long_name"]
                if data[i]["types"][0]=="postal_code":
                    response_data["pin_code"] = data[i]["long_name"]
            response_data['status'] = 1
            response_data['massage'] = "Saved Successfully"
            return Response(response_data, status=200)
        else:
            response_data['status'] = 0
            response_data['massage'] = "Cannot Able to address"
            return Response(response_data, status=204)


class Protfolio(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        response_data = {}
        user = request.user
        user_id = user.id
        requestdata = request.data
        rs = User.objects.filter(id=user_id, is_active=True, is_blocked=False, is_deleted=False).first()
        if rs:
            checkp = Profileinfo.objects.filter(user_id=user_id)
            if checkp:
                obj = Profileinfo.objects.filter(user_id=user_id).update(
                Information=requestdata['about_me'],
                philisophy=request.data['philisophy'],
                achievements=request.data['achievements'],
                toprecipe=request.data['toprecipe'],
                foodoftheweek=request.data['foodoftheweek']
                )
                response_data['status'] = 1
                response_data['massage'] = "Invalid Request"
                http_status_code = 200
            else:
                obj = Profileinfo.objects.create(
                user_id=user_id,
                Information=requestdata['about_me'],
                philisophy=request.data['philisophy'],
                achievements=request.data['achievements'],
                toprecipies=request.data['toprecipe'],
                foodoftheweek=request.data['foodoftheweek']
                )
                response_data['status'] = 1
                response_data['massage'] = "Cannot Able to address"
                http_status_code = 200
        else:
            response_data['status'] = 0
            response_data['massage'] = "Cannot Able to address"
            http_status_code = 400
        return Response(response_data, status=http_status_code)

    # def put(self, request):
    #     response_data = {}
    #     user = request.user
    #     user_id = user.id
    #     requestdata = request.data
    #     rs = User.objects.filter(id=user_id, is_active=True, is_blocked=False, is_deleted=False).first()
    #     if rs:
    #         obj = User.objects.filter(user_id=user_id).update(
    #             Information=requestdata['Information']
    #         )
    #         response_data['status'] = 1
    #         response_data['massage'] = "Cannot Able to address"
    #         http_status_code = 200
    #     else:
    #         response_data['status'] = 0
    #         response_data['massage'] = "Cannot Able to address"
    #         http_status_code = 400
    #     return Response(response_data, status=http_status_code)


class Subscribe(generics.ListAPIView):

    def post(self, request, format=None):
        response_data = {}
        requestdata = request.data
        email=requestdata['email']
        if email:
            sent =send_mail_otp(email)
            response_data['status'] = 1
            response_data['massage'] = "Cannot Able to address"
            http_status_code = 200
        else:
            response_data['status'] = 0
            response_data['massage'] = "Cannot Able to address"
            http_status_code = 400
        return Response(response_data, status=http_status_code)


def send_mail_otp(receiver_mail):
    msg = EmailMessage()
    msg['Subject'] = 'Thanking for Subscribing us '
    msg['From'] = "no-reply@thorsignia.online.naresh@thorsignia.online" 
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
    s.login("no-reply@bakeapp.naresh@thorsignia.online","Naresh@9902")
    s.sendmail("no-reply@bakeapp.naresh@thorsignia.online", receiver_mail, msg.as_string())
    return True
    
    
    

class Sendmail(generics.ListAPIView):

    def post(self, request, format=None):
        response_data = {}
        requestdata = request.data
 
        category=requestdata['category']
      
        if category:
            sent =send_mail_otp(category)
            response_data['status'] = 1
            response_data['massage'] = "Cannot Able to address"
            http_status_code = 200
        else:
            response_data['status'] = 0
            response_data['massage'] = "Cannot Able to address"
            http_status_code = 400
        return Response(response_data, status=http_status_code)


def send_mail_otp(category):
    msg = EmailMessage()
    msg['Subject'] = 'Request new category'
    msg['From'] = "noreply@byhomechefs.com" 
    msg['To'] = "noreply@byhomechefs.com"
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
            border: 3px solid rgba(243,161,163,1); 
            background-color: rgba(255,249,248,1);
            height: 100%;font-family:'Poppins', sans-serif;;">
            <div style="padding-left: 40px;margin-top: 10px;  font-size: 15px;">
                <p style="font-size: 15px;font-weight: 600;">Request for New Category  </p>
                <p >Category Name : '''+str(category)+''' <br> 
                </p>
            </div>
           
       
          </div>
      </body>
    </html>
    ''', subtype='html')
    s = smtplib.SMTP('naresh11021@gmail.com') 
    s.starttls()
    s.login("naresh11021@gmail.com","7026677055")
    #s.sendmail("no-reply@petapp.naresh@thorsignia.online", receiver_mail, msg.as_string())
    s.sendmail("naresh11021@gmail.com", "naresh11021@gmail.com", msg.as_string())
    return True
