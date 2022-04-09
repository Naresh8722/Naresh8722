from django.db.models import query
from rest_framework.response import Response
from user.serializers import *
from rest_framework.views import APIView
import math, random
from twilio.rest import Client
import json
import requests
import smtplib,ssl
from email.message import EmailMessage
from rest_framework.permissions import IsAuthenticated

# account_sid = 'AC4206d6db4fe92e8f8033110f49f720de'
# auth_token = '45736e30fb44cab4c98551f48573635a'
# client = Client(account_sid, auth_token)
# url = "https://www.fast2sms.com/dev/bulk"
url = "https://www.fast2sms.com/dev/bulkV2"
# url = "https://www.fast2sms.com/dev/bulkV2"
#### FAST2SMS Gateway conf

port = 587
smtp_server ="smtp.gmail.com"
sender_email = "naresh11021@gmail.com"
password = "7026677055"

###############################################################################
#For Customer

class MobileDetailsViewCustomer(APIView):
    def post(self, request, *args, **kwargs):
        response_data = request.data
        mobile = request.data.get('mobile')
        response = {}
        rs = User.objects.filter(phone_no=mobile,user_type=1,is_blocked=False, is_deleted=False)
        if rs:
            for i in rs:
                user_id=i.id
            otp = generate_otp(mobile)
            message =sendsms(mobile,otp)
            if message:
                save_db={}
                save_db['created_date'] = timezone.now()
                save_db['mobile'] = mobile
                save_db['otp'] = otp
                save_db['user']=user_id
                save_db['modified_date'] = timezone.now()
                serializer = MobileViewSerializer(data=save_db)
                if serializer.is_valid():
                    user = OTP.objects.filter(mobile=mobile).first()
                    if not user:
                        serializer.save()
                        response['status'] = 1
                        response['msg'] = 'OTP Sent'
                        http_status_code = 200
                    else:
                        OTP.objects.filter(mobile=mobile).update(otp=otp)
                        response['status'] = 1
                        response['msg'] = 'OTP Sent'
                        http_status_code = 200
                else:
                    response['status'] = 0
                    http_status_code = 404
            else:
                response['status'] = 0
                response['msg'] = 'OTP cannot be sent!!'
                http_status_code = 404

        else:
            response['status'] = 0
            response['msg'] = 'No user found'
            http_status_code = 404
        return Response(response, status=http_status_code)


class EmailDetailsViewCustomer(APIView):
    
    # serializer_class=EmailViewSerializer
    def post(self, request, *args, **kwargs):
        response_data = request.data
        email = response_data('email')
        print(email)
        response = {}
        rs = User.objects.filter(email=email,is_blocked=False,is_deleted=False)
        print(rs)
        if rs:
            for i in rs:
                user_id=i.id
            otp = generateEmail_otp(email)
            message =send_mail_otp(otp,email)
            if message:
                save_db={}
                save_db['created_date'] = timezone.now()
                # if email != user.email:
                #     try:
                #         subject = 'Request for adding a category/product'
                #         message = 'I am requestion for approval of adding a new oroduct/category'
                #         recepient = str(sub['Email'].value())
                #         send_mail(subject, 
                #             message, user.email, [], fail_silently = False)
                #         return JsonResponse({'status': 1, 'msg': 'Email sent successfully'}, status=200)
                    # except:
                save_db['email'] = email
                save_db['verification_code'] = otp
                save_db['user']=user_id
                save_db['modified_date'] = timezone.now()
                serializer = EmailViewSerializer(data=save_db)
                if serializer.is_valid():
                    user = EmailCodeVerification.objects.filter(user_id=user_id,is_deleted=False).first()
                    if not user:
                        serializer.save()
                        response['status'] = 1
                        response['msg'] = 'OTP Sent'
                        http_status_code = 200
                    else:
                        EmailCodeVerification.objects.filter(user_id=user_id).update(verification_code=otp)
                        response['status'] = 1
                        response['msg'] = 'OTP Sent'
                        http_status_code = 200
                else:
                    response['status'] = 0
                    http_status_code = 404
            else:
                response['status'] = 0
                response['msg'] = 'OTP cannot be sent!!'
                http_status_code = 404

        else:
            response['status'] = 0
            response['msg'] = 'No user found'
            http_status_code = 404
        print(response)
        return Response(response, status=http_status_code)

class OtpVerificationViewCustomer(APIView):
    def post(self, request, *args, **kwargs):
        response_data = request.data
        otp = request.data.get('otp')
        phone_no = request.data.get('mobile')
        # otp = "".join(str(x) for x in otp)
        user_id = Users.objects.filter(phone_no=phone_no).values('id').distinct()
        user_id = user_id[0]['id']
        rs=OTP.objects.filter(user_id=user_id).values('otp','modified_date').distinct()
        generated_otp = rs[0]['otp']
        response = {}
        validity = timezone.now() - rs[0]['modified_date']
        rs = Users.objects.filter(id=user_id, user_type=1, is_active=True, is_blocked=False, is_deleted=False)
        if rs:
            print(otp)
            print(generated_otp)
            if int(otp) == generated_otp:
                
                user_access = Users.objects.filter(phone_no=phone_no,user_type=1).values('account').distinct()
                user_update = Users.objects.filter(id=user_id).update(is_phone_verified=True)
                otp_update = OTP.objects.filter(user_id=user_id).update(is_verified=int(True))
                response['status'] = 1
                response['msg'] = 'OTP Verified'
                response['p']= user_access[0]['account']
                http_status_code = 200
            else:
                user_update = Users.objects.filter(id=user_id).update(is_phone_verified=False)
                otp_update = OTP.objects.filter(user_id=user_id).update(is_verified=int(False))
                response['status'] = 0
                response['msg'] = 'Incorrect Otp'
                http_status_code = 200
        else:
            response['status'] = 0
            response['msg'] = 'No user found'
            http_status_code = 404
        return Response(response, status=http_status_code)

class EmailOtpVerificationViewCustomer(APIView):
    def post(self, request, *args, **kwargs):
        response_data = request.data
        otp = request.data.get('otp')
        # otp="".join(str(x) for x in otp)
        print(otp)
        email = request.data.get('email')
        user_id = User.objects.filter(email=email,user_type=1).values('id').distinct()
        user_id = user_id[0]['id']
        rs=EmailCodeVerification.objects.filter(user_id=user_id).values('verification_code','modified_date').distinct()
        generated_otp = rs[0]['verification_code']
        response = {}
        validity = timezone.now() - rs[0]['modified_date']
        rs = User.objects.filter(id=user_id, is_active=True, is_blocked=False, is_deleted=False)
        if rs:
            if otp == generated_otp:
                # user_access = User.objects.filter(email=email).values('account').distinct()
                user_update = Users.objects.filter(id=user_id).update(is_email_verified=True)
                otp_update = EmailCodeVerification.objects.filter(user_id=user_id).update(is_varified=int(True))
                response['status'] = 1
                response['msg'] = 'Otp Verified'
                http_status_code = 200
            else:
                user_update = Users.objects.filter(id=user_id).update(is_email_verified=False)
                otp_update = EmailCodeVerification.objects.filter(user_id=user_id).update(is_varified=int(False))
                response['status'] = 0
                response['msg'] = 'Incorrect Otp'
                http_status_code = 202
        else:
            response['status'] = 0
            response['msg'] = 'No user found'
            http_status_code = 404
        return Response(response, status=http_status_code)


################################################################################
#For Vendor

class MobileDetailsView(APIView):
    def post(self, request, *args, **kwargs):
        response_data = request.data
        mobile = request.data.get('mobile')
        response = {}
        rs = User.objects.filter(phone_no=mobile, is_blocked=False,user_type=2,is_deleted=False)
        if rs:
            for i in rs:
                user_id=i.id
            otp = generate_otp(mobile)
            message =sendsms(mobile,otp)
            if message:
                save_db={}
                save_db['created_date'] = timezone.now()
                save_db['mobile'] = mobile
                save_db['otp'] = otp
                save_db['user']=user_id
                save_db['modified_date'] = timezone.now()
                serializer = MobileViewSerializer(data=save_db)
                if serializer.is_valid():
                    user = OTP.objects.filter(mobile=mobile).first()
                    if not user:
                        serializer.save()
                        response['status'] = 1
                        response['msg'] = 'OTP Sent'
                        http_status_code = 200
                    else:
                        OTP.objects.filter(mobile=mobile).update(otp=otp)
                        response['status'] = 1
                        response['msg'] = 'OTP Sent'
                        http_status_code = 200
                else:
                    response['status'] = 0
                    http_status_code = 404
            else:
                response['status'] = 0
                response['msg'] = 'OTP cannot be sent!!'
                http_status_code = 404

        else:
            response['status'] = 0
            response['msg'] = 'No user found'
            http_status_code = 404
        return Response(response, status=http_status_code)


class EmailDetailsView(APIView):
    query_set=''
    def post(self, request, *args, **kwargs):
        response_data = request.data
        email = request.data.get('email')
        response = {}
        rs = Users.objects.filter(email=email,is_blocked=False, is_deleted=False)
        print(rs)
        if rs:
            for i in rs:
                user_id=i.id
            otp = generateEmail_otp(email)
            message =send_mail_otp(otp,email)
            if message:
                save_db={}
                save_db['created_date'] = timezone.now()
                # if email != user.email:
                #     try:
                #         subject = 'Request for adding a category/product'
                #         message = 'I am requestion for approval of adding a new oroduct/category'
                #         recepient = str(sub['Email'].value())
                #         send_mail(subject, 
                #             message, user.email, [], fail_silently = False)
                #         return JsonResponse({'status': 1, 'msg': 'Email sent successfully'}, status=200)
                    # except:
                save_db['email'] = email
                save_db['verification_code'] = otp
                save_db['user']=user_id
                save_db['modified_date'] = timezone.now()
                serializer = EmailViewSerializer(data=save_db)
                if serializer.is_valid():
                    user = EmailCodeVerification.objects.filter(user_id=user_id,is_deleted=False).first()
                    if not user:
                        serializer.save()
                        response['status'] = 1
                        response['msg'] = 'OTP Sent'
                        http_status_code = 200
                    else:
                        EmailCodeVerification.objects.filter(user_id=user_id).update(verification_code=otp)
                        response['status'] = 1
                        response['msg'] = 'OTP Sent'
                        http_status_code = 200
                else:
                    response['status'] = 0
                    http_status_code = 404
            else:
                response['status'] = 0
                response['msg'] = 'OTP cannot be sent!!'
                http_status_code = 404

        else:
            response['status'] = 0
            response['msg'] = 'No user found'
            http_status_code = 404
        print(response)
        return Response(response, status=http_status_code)


class ChangeNumberOtp(APIView):
    permission_classes = (IsAuthenticated,)
    # queryset=''
    # serializer_class=MobileViewSerializer
    def post(self, request, *args, **kwargs):
        response_data = request.data
        user = request.user
        user_id = user.id
        mobile = request.data.get('mobile')
        response = {}
        rs = User.objects.filter(id=user_id, is_blocked=False, is_deleted=False)
        if rs:
            otp = generate_otp(mobile)
            message =sendsms(mobile,otp)
            if message:
                save_db={}
                save_db['created_date'] = timezone.now()
                save_db['mobile'] = mobile
                save_db['otp'] = otp
                save_db['user']=user_id
                save_db['modified_date'] = timezone.now()
                serializer = MobileViewSerializer(data=save_db)
                if serializer.is_valid():
                    user = OTP.objects.filter(mobile=mobile).first()
                    if not user:
                        serializer.save()
                        response['status'] = 1
                        response['msg'] = 'OTP Sent'
                        http_status_code = 200
                    else:
                        OTP.objects.filter(mobile=mobile).update(otp=otp)
                        response['status'] = 1
                        response['msg'] = 'OTP Sent'
                        http_status_code = 200
                else:
                    response['status'] = 0
                    http_status_code = 404
            else:
                response['status'] = 0
                response['msg'] = 'OTP cannot be sent!!'
                http_status_code = 404
        else:
            response['status'] = 0
            response['msg'] = 'No user found'
            http_status_code = 404
        return Response(response, status=http_status_code)

class ChangeEmailAddress(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        response_data = request.data
        user = request.user
        user_id = user.id
        email = request.data.get('email')
        response = {}
        rs = User.objects.filter(id=user_id,is_blocked=False, is_deleted=False)
        if rs:
            for i in rs:
                user_id=i.id
            otp = generateEmail_otp(email)
            message =send_mail_otp(otp,email)
            if message:
                save_db={}
                save_db['created_date'] = timezone.now()
                save_db['email'] = email
                save_db['verification_code'] = otp
                save_db['user']=user_id
                save_db['modified_date'] = timezone.now()
                serializer = EmailViewSerializer(data=save_db)
                if serializer.is_valid():
                    user = EmailCodeVerification.objects.filter(email=email,is_deleted=False).first()
                    if not user:
                        serializer.save()
                        response['status'] = 1
                        response['msg'] = 'OTP Sent'
                        response['details'] = serializer.data
                        http_status_code = 200
                    else:
                        EmailCodeVerification.objects.filter(email=email).update(verification_code=otp)
                        response['status'] = 1
                        response['msg'] = 'OTP Sent'
                        http_status_code = 200
                else:
                    response['status'] = 0
                    http_status_code = 404
            else:
                response['status'] = 0
                response['msg'] = 'OTP cannot be sent!!'
                http_status_code = 404

        else:
            response['status'] = 0
            response['msg'] = 'No user found'
            http_status_code = 404
        return Response(response, status=http_status_code)

from django.templatetags.static import static

def send_confirm_mail(receiver_mail):
    msg = EmailMessage()
    msg['Subject'] = 'Message from By Home Chefs'
    msg['From'] = "nareshmv11021@gmail.com" 
    msg['To'] = receiver_mail
    img_url = static('assets/images/email.jpeg')
    msg.set_content('''
    <!DOCTYPE html>
    <html>
        <head>
          <!-- Required meta tags -->
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
      </head>
      <body>
        <img src="https://naresh11021@gmail.com/email.jpeg" width="100%" height="100%">
      </body>
    </html>
    ''', subtype='html')
    s = smtplib.SMTP('587') 
    s.starttls()
    s.login("nareshmv11021@gmail.com","qrbowiisdwrviswg")
    s.sendmail("nareshmv11021@gmail.com", receiver_mail, msg.as_string())
    return True

def send_confirm_mail_admin():
    msg = EmailMessage()
    msg['Subject'] = 'New Vendor'
    msg['From'] = "nareshmv11021@gmail.com" 
    msg['To'] = "nareshmv11021@gmail.com"
    msg.set_content('''
    <!DOCTYPE html>
    <html>
        <head>
          <!-- Required meta tags -->
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
      </head>
      <body>
        <h2>The new vendor has signup now</h2>
        
      </body>
    </html>
    ''',subtype='html')
    s = smtplib.SMTP('587') 
    s.starttls()
    s.login("naresh11021@gmail.com","qrbowiisdwrviswg")
    s.sendmail("naresh11021@gmail.com", "naresh11021@gmail.com", msg.as_string())
    return True


def send_mail_otp(otp,receiver_mail):
    
    s = smtplib.SMTP('587')
    msg = EmailMessage()
    msg['Subject'] = 'Email Verification Code'
    msg['From'] = "naresh11021@gmail.com" 
    msg['To'] = receiver_mail
    new="Your Email Verification otp is:"+str(otp)
    msg.set_content(new)
    s.starttls()
    
    s.login("naresh11021@gmail.com","7026677055")
    s.sendmail("naresh11021@gmail.com", receiver_mail, msg.as_string()) 
    s.quit() 
    return True
    

#### Send Otp from Login With Otp Page
class LoginWithotpView(APIView):
    def post(self, request, *args, **kwargs):
        mobile = request.data.get('userPhone')
        response = {}
        rs = User.objects.filter(phone_no=mobile, is_active=True, is_blocked=False, is_deleted=False)
        if rs:
            for i in rs:
                user_id = i.id
            otp = generate_otp(mobile)
            message =sendsms(mobile,otp)
            if message:
                save_db = {}
                save_db['created_date'] = timezone.now()
                save_db['mobile'] = mobile
                save_db['otp'] = otp
                save_db['user'] = user_id
                save_db['modified_date'] = timezone.now()
                serializer = MobileViewSerializer(data=save_db)
                if serializer.is_valid():
                    user = OTP.objects.filter(user_id=user_id, is_deleted=False).first()
                    if not user:
                        serializer.save()
                        response['status'] = 1
                        response['msg'] = 'OTP Sent'
                        response['details'] = serializer.data
                        http_status_code = 200
                    else:
                        OTP.objects.filter(user_id=user_id).update(otp=otp)
                        response['status'] = 1
                        response['msg'] = 'OTP  Sent'
                        http_status_code = 200
                else:
                    response['status'] = 0
                    http_status_code = 404
            else:
                response['status'] = 0
                response['msg'] = 'OTP cannot be sent!!'
                http_status_code = 404
        else:
            response['status'] = 0
            response['msg'] = 'No user found'
            http_status_code = 404
        return Response(response, status=http_status_code)


class SellerUserLoginOtpView(APIView):
    def post(self, request, *args, **kwargs):
        response_data = request.data
        # print(request.POST)
        mobile = request.data.get('mobile')
        response = {}
        rs = User.objects.filter(phone_no=mobile, is_active=True, is_blocked=False, is_deleted=False)
        for i in rs:
            user_id= rs.id
        if rs:
            otp = generate_otp(mobile)
            message =sendsms(mobile,otp)
            if message:
                save_db={}
                save_db['created_date'] = timezone.now()
                save_db['mobile'] = mobile
                save_db['otp'] = otp
                save_db['user']=user_id
                save_db['modified_date'] = timezone.now()
                serializer = MobileViewSerializer(data=save_db)
                if serializer.is_valid():
                    user = OTP.objects.filter(user_id=user_id,is_deleted=False).first()
                    if not user:
                        serializer.save()
                        response['status'] = 1
                        response['msg'] = 'OTP Sent'
                        response['details'] = serializer.data
                        http_status_code = 200
                    else:
                        OTP.objects.filter(user_id=user_id).update(otp=otp)
                        response['status'] = 1
                        response['msg'] = 'OTP Sent'
                        http_status_code = 200
                else:
                    response['status'] = 0
                    http_status_code = 404
            else:
                response['status'] = 0
                response['msg'] = 'OTP cannot be sent!!'
                http_status_code = 404

        else:
            response['status'] = 0
            response['msg'] = 'No user found'
            http_status_code = 404
        return Response(response, status=http_status_code)


def sendsms(number, msg):
    payload = {
        'sender_id': 'FSTSMS',
        'message': "Your Otp for Registration is "+str(msg),
        'language': 'english',
        'route': 'p',
        'numbers': number
    }
    headers = { 
         'authorization':"XSpv592P6EdHAzQxeaOCj0cRWghoGKrlJ1Bb4kZwTFNn8VquLDOqoXPKJyHfC8g4hzFjUVuwRpiT3Ev9" , 
    ##'authorization': "Cr79v4zuMHiWcBFm8YK2ElxyqVGR3bALTkIwt1Safp0eQN6XhUkVyhIE9UD1B2opGNCdjHRKgvcWbSm5", 
    # 'authorization': "9iqLkXfIm3GNWPUd05tolCD71Rb6xsTnegHSEJupcwaAyM4KrvF0jY1rLgcUqG9bnihO7wKDJEMxsZXd", 
    'Content-Type': "application/x-www-form-urlencoded", 
    'Cache-Control': "no-cache"
}
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    return response.text

def generate_otp(mobile):
    if mobile:
        digits = '0123456789'
        new_otp = ''
        for i in range(4):
            new_otp += digits[math.floor(random.random() * 10)]
        return new_otp
    else:
        return False


def generateEmail_otp(mobile):
    if mobile:
        digits = '0123456789'
        new_otp = ''
        for i in range(4):
            new_otp += digits[math.floor(random.random() * 10)]
        return new_otp
    else:
        return False


class OtpVerificationView(APIView):
    def post(self, request, *args, **kwargs):
        response_data = request.data
        otp = request.data.get('otp')
        phone_no = request.data.get('phone_no')
        # otp = "".join(str(x) for x in otp)
        user_ids = User.objects.filter(phone_no=phone_no,user_type=2).values('id','email').distinct()
        user_id = user_ids[0]['id']
        rs=OTP.objects.filter(user_id=user_id).values('otp','modified_date').distinct()
        generated_otp = rs[0]['otp']
        response = {}
        validity = timezone.now() - rs[0]['modified_date']
        rs = User.objects.filter(id=user_id, is_active=True, is_blocked=False, is_deleted=False)
        if rs:
            if otp == generated_otp:
                user_access = User.objects.filter(phone_no=phone_no).values('account').distinct()
                user_update = Users.objects.filter(id=user_id).update(is_phone_verified=True)
                otp_update = OTP.objects.filter(user_id=user_id).update(is_verified=int(True))
                send_confirm_mail(user_ids[0]['email'])
                send_confirm_mail_admin()
                response['status'] = 1
                response['msg'] = 'OTP Verified'
                response['p']= user_access[0]['account']
                http_status_code = 200
            else:
                user_update = Users.objects.filter(id=user_id).update(is_phone_verified=False)
                otp_update = OTP.objects.filter(user_id=user_id).update(is_verified=int(False))
                response['status'] = 0
                response['msg'] = 'Incorrect Otp'
                http_status_code = 200
        else:
            response['status'] = 0
            response['msg'] = 'No user found'
            http_status_code = 404
        return Response(response, status=http_status_code)

class VerifySecondaryNumber(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        response_data = request.data
        otp = request.data.get('otp')
        phone_no = request.data.get('phone_no')
        otp = "".join(str(x) for x in otp)
        user = request.user
        user_id = user.id
        rs=OTP.objects.filter(mobile=phone_no).values('otp','modified_date').distinct()
        generated_otp = rs[0]['otp']
        response = {}
        validity = timezone.now() - rs[0]['modified_date']
        rs = User.objects.filter(id=user_id, is_active=True, is_blocked=False, is_deleted=False)
        if rs:
            if otp == generated_otp:
                user_update = Users.objects.filter(id=user_id).update(secondary_no=phone_no)
                response['status'] = 1
                response['msg'] = 'OTP Verified'
                # response['p']= user_access[0]['account']
                http_status_code = 200
            else:
                response['status'] = 0
                response['msg'] = 'Incorrect Otp'
                http_status_code = 200
        else:
            response['status'] = 0
            response['msg'] = 'No user found'
            http_status_code = 404
        return Response(response, status=http_status_code)

class NumberChangeVerificationView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        response_data = request.data
        otp = request.data.get('otp')
        phone_no = request.data.get('phone_no')
        otp = "".join(str(x) for x in otp)
        user = request.user
        user_id = user.id
        rs=OTP.objects.filter(mobile=phone_no).values('otp','modified_date').distinct()
        generated_otp = rs[0]['otp']
        response = {}
        validity = timezone.now() - rs[0]['modified_date']
        rs = User.objects.filter(id=user_id, is_active=True, is_blocked=False, is_deleted=False)
        if rs:
            print(otp)
            print(generated_otp)
            if otp == generated_otp:
                user_update = Users.objects.filter(id=user_id).update(phone_no=phone_no)
                response['status'] = 1
                response['msg'] = 'OTP Verified'
                # response['p']= user_access[0]['account']
                http_status_code = 200
            else:
                response['status'] = 0
                response['msg'] = 'Incorrect Otp'
                http_status_code = 200
        else:
            response['status'] = 0
            response['msg'] = 'No user found'
            http_status_code = 404
        return Response(response, status=http_status_code)


class EmailOtpVerificationView(APIView):
    def post(self, request, *args, **kwargs):
        response_data = request.data
        otp = request.data.get('otp')
        otp="".join(str(x) for x in otp)
        print(otp)
        email = request.data.get('email')
        user_id = User.objects.filter(email=email).values('id').distinct()
        user_id = user_id[0]['id']
        rs=EmailCodeVerification.objects.filter(user_id=user_id).values('verification_code','modified_date').distinct()
        generated_otp = rs[0]['verification_code']
        response = {}
        validity = timezone.now() - rs[0]['modified_date']
        rs = User.objects.filter(id=user_id, is_active=True, is_blocked=False, is_deleted=False)
        if rs:
            if otp == generated_otp:
                # user_access = User.objects.filter(email=email).values('account').distinct()
                user_update = Users.objects.filter(id=user_id).update(is_email_verified=True)
                otp_update = EmailCodeVerification.objects.filter(user_id=user_id).update(is_varified=int(True))
                response['status'] = 1
                response['msg'] = 'Otp Verified'
                http_status_code = 200
            else:
                user_update = Users.objects.filter(id=user_id).update(is_email_verified=False)
                otp_update = EmailCodeVerification.objects.filter(user_id=user_id).update(is_varified=int(False))
                response['status'] = 0
                response['msg'] = 'Incorrect Otp'
                http_status_code = 202
        else:
            response['status'] = 0
            response['msg'] = 'No user found'
            http_status_code = 404
        return Response(response, status=http_status_code)


class EmailChangeVerificationView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        response_data = request.data
        otp = request.data.get('otp')
        otp="".join(str(x) for x in otp)
        user = request.user
        user_id = user.id
        email = request.data.get('email')
        rs=EmailCodeVerification.objects.filter(email=email).values('verification_code','modified_date').distinct()
        generated_otp = rs[0]['verification_code']
        response = {}
        validity = timezone.now() - rs[0]['modified_date']
        rs = User.objects.filter(id=user_id, is_active=True, is_blocked=False, is_deleted=False)
        if rs:
            if otp == generated_otp:
                user_update = Users.objects.filter(id=user_id).update(email=email)
                response['status'] = 1
                response['msg'] = 'Otp Verified'
                http_status_code = 200
            else:
                response['status'] = 0
                response['msg'] = 'Incorrect Otp'
                http_status_code = 202
        else:
            response['status'] = 0
            response['msg'] = 'No user found'
            http_status_code = 404
        return Response(response, status=http_status_code)