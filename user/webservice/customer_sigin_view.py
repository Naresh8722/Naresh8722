from django.db.models import query, query_utils
from django.db.models.query import QuerySet
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from django.http import HttpResponse
from user.serializers import *
from django.utils import timezone
import base64
from slugify import slugify
import random
from django.db.models import Q
from rest_framework.views import APIView


class JSONResponse(HttpResponse):
    """ An HttpResponse that renders its content into JSON. """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


# ////////////////////////////  CUSTOMER REG LOGIN //////////////////////////////////////////////


class CustomerRegistrationView(generics.ListAPIView):
    queryset = ''
    serializer_class = CustomerSignupSerializer
    def post(self, request):
        serializer = CustomerSignupSerializer(data=request.data)
        if serializer.is_valid():           
            print("started validation")
            requestData = serializer.validated_data
            print(requestData)
            email = requestData['email']
            password = requestData['password']
            phone_no = requestData['phone_no']
            referelcode ='home'+str(random.randint(10000000, 99999999))
            wallet=0
            p_d=password
            account = account_encoder(p_d)
            username = email.split("@")[0]

            ## check Email aiiready exist or not
            user = User.objects.filter(email=email,is_deleted=False,user_type=1).count()            
            user_no = User.objects.filter(phone_no=phone_no, is_deleted=False,user_type=1).count()
            usernm = User.objects.filter(username=username,is_deleted=False,user_type=1).count()  
            print("=================",user,usernm,user_no)
            if usernm>0:
                username=username+str(random.randint(1000, 9999))
            if user > 0:
                msg = {"Unauthorized error ": ['Email already Registered....', ]}
                errors = {'errors': msg}
                return JSONResponse(errors, status=401)
            elif user_no >0:
                msg = {"Unauthorized error ": ['Mobile Already Registered....', ]}
                errors = {'errors': msg}
                return JSONResponse(errors, status=401)
            else:
                obj = User.objects.create_user( 
                    email=email,
                    phone_no=phone_no,
                    username=username,
                    account=account,
                    referelcode = referelcode,
                    wallet=wallet,
                    is_staff=False,
                    is_superuser=False,
                    is_phone_verified=True,
                    is_email_verified=True,
                    is_active=True,
                    user_type=1
                )
                obj.set_password(password)
                obj.save()
                data = {
                    'status': 1,
                    'id': obj.id,
                    'email': obj.email,
                    'username': obj.username,
                    'message': 'Customer created successfully'
                }
                return JSONResponse(data, status=200)
        else:
            return JsonResponse({'msg': 'Email Or Password did not match'}, status=400)

class CustomerLoginView(generics.ListAPIView):
    queryset = ""
    serializer_class = CustomerLoginSerializer
    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        if serializer.is_valid():
            mobile = request.data['phone_no']
            email = request.data['email']
            password = request.data['password']
            User = get_user_model()
            #user = User.objects.filter((Q(email=email)|Q(phone_no=mobile)),user_type=1, is_deleted=False, is_blocked=False).first()
            user = User.objects.filter(email=email,user_type=1, is_deleted=False, is_blocked=False).first()
            if user:
                if user.check_password(password):  ## Check password matched or not
                    if user.is_phone_verified:
                        if user.is_email_verified:  ## Check user phone is verified or not
                            if user.is_active:  ## Check user active or deactive
                                token, created = Token.objects.get_or_create(
                                    user=user)  ### Get user authentication token
                                token_data = token.key  ### if it is first login then create token first and get token
                                user.last_login = timezone.now()
                                user.save()
                                serialize_userdata = {
                                    'status': 1,
                                    'id': user.id,
                                    'email': user.email,
                                    'phone_no':user.phone_no,
                                    'username': user.username,
                                    'token': token_data,
                                    'first_name': user.first_name,
                                    'last_name': user.last_name,
                                    'is_superuser': user.is_superuser,
                                    'is_active': user.is_active,
                                    'is_staff': user.is_staff,
                                    'last_login': user.last_login
                                }
                                # return JSONResponse(serialize_userdata, status=200)
                                return JSONResponse({'status': 0, 'msg': 'Login Successfull'}, status=200)
                            else:
                                return JSONResponse({'status': 0, 'msg': 'Your account is not activated.'}, status=200)
                        else:
                            return JsonResponse({'status': 4, 'msg': 'Email is not verified',"email":user.email}, status=202)
                    else:
                        if user.is_email_verified:
                            return JsonResponse({'status': 2, 'msg': 'Your Mobile Number is not verified'}, status=202)
                        else:
                            return JsonResponse({'status': 3, 'msg': 'Your Mobile Number & email is not verified',"email":user.email}, status=202)
                else:
                    return JsonResponse({'status': 0, 'msg': 'Password did not match'}, status=200)
            else:
                return JsonResponse({'status': 0, 'msg': 'Mobile Number did not match'}, status=200)
            
        else:
            return JsonResponse({'msg': 'Mobile Or Password did not match serializer'}, status=401)


class CustomerLoginOtpView(generics.ListAPIView):
    queryset=OTP.objects.all()
    serializer_class=MobileViewSerializer
    def post(self, request):
        phone_no = request.data.get('mobile')
        User = get_user_model()
        try:  ## Check user Number Exist
            user = User.objects.filter(phone_no=phone_no,user_type=1,is_deleted=False, is_blocked=False).first()
            if user:
                if user.is_active:  ## Check user active or deactive
                    print(user.is_active)
                    token, created = Token.objects.get_or_create(
                        user=user)  ### Get user authentication token
                    token_data = token.key  ### if it is first login then create token first and get token
                    user.last_login = timezone.now()
                    user.save()
                    serialize_userdata = {
                        'status': 1,
                        'id': user.id,
                        'email': user.email,
                        'phone_no': user.phone_no,
                        'username': user.username,
                        'token': token_data,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'is_superuser': user.is_superuser,
                        'is_active': user.is_active,
                        'is_staff': user.is_staff,
                        'last_login': user.last_login,
                    }
                    #return JSONResponse(serialize_userdata, status=200)
                    return JSONResponse({'status': 1, 'msg': 'Login Successfull'}, status=200)
                else:
                    return JSONResponse({'status': 0, 'msg': 'Your account is not acivated.'}, status=200)
            else:
                    return JsonResponse({'status': 0, 'msg': 'Mobile Number did not match'}, status=200)
        except User.DoesNotExist:
                return JSONResponse({'status': 0, 'msg': 'Authentication Error'}, status=401)
        else:
            return JsonResponse({'msg': 'Mobile Or Password did not match'}, status=401)

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class SellerUserLoginView(generics.ListAPIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            requestData = serializer.validated_data
            mobile = requestData['phone_no']
            password = requestData['password']
            User = get_user_model()
            try:  ## Check user Number Exist
                user = User.objects.filter(phone_no=mobile, is_deleted=False, is_blocked=False).first()
                if user:
                    if user.check_password(password):  ## Check password matched or not
                        if user.is_phone_verified:  ## Check user phone is verified or not
                            if user.is_active:  ## Check user active or deactive
                                token, created = Token.objects.get_or_create(
                                    user=user)  ### Get user authentication token
                                token_data = token.key  ### if it is first login then create token first and get token
                                user.last_login = timezone.now()
                                user.save()
                                serialize_userdata = {
                                    'status': 1,
                                    'id': user.id,
                                    'email': user.email,
                                    'phone_no':user.phone_no,
                                    'username': user.username,
                                    'token': token_data,
                                    'first_name': user.first_name,
                                    'last_name': user.last_name,
                                    'is_superuser': user.is_superuser,
                                    'is_active': user.is_active,
                                    'is_staff': user.is_staff,
                                    'last_login': user.last_login
                                }
                                return JSONResponse(serialize_userdata, status=200)
                            else:
                                return JSONResponse({'status': 0, 'msg': 'Your account is not acivated.'}, status=200)
                        else:
                            return JsonResponse({'status': 2, 'msg': 'Your Mobile Number is not verified'}, status=202)
                    else:
                        return JsonResponse({'status': 0, 'msg': 'Password did not match'}, status=200)
                else:
                    return JsonResponse({'status': 0, 'msg': 'Mobile Number did not match'}, status=200)
            except User.DoesNotExist:
                return JSONResponse({'status': 0, 'msg': 'Authentication Error'}, status=401)
        else:
            return JsonResponse({'msg': 'Mobile Or Password did not match'}, status=401)


class SellerUserLoginOtpView(generics.ListAPIView):
    def post(self, request):
        phone_no = request.data.get('phone_no')
        User = get_user_model()
        try:  ## Check user Number Exist
            user = User.objects.filter(phone_no=phone_no, is_deleted=False, is_blocked=False).first()
            if user:
                if user.is_active:  ## Check user active or deactive
                    print(user.is_active)
                    token, created = Token.objects.get_or_create(
                        user=user)  ### Get user authentication token
                    token_data = token.key  ### if it is first login then create token first and get token
                    user.last_login = timezone.now()
                    user.save()
                    serialize_userdata = {
                        'status': 1,
                        'id': user.id,
                        'email': user.email,
                        'phone_no': user.phone_no,
                        'username': user.username,
                        'token': token_data,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'is_superuser': user.is_superuser,
                        'is_active': user.is_active,
                        'is_staff': user.is_staff,
                        'last_login': user.last_login,
                    }
                    print(serialize_userdata)
                    return JSONResponse(serialize_userdata, status=200)
                else:
                    return JSONResponse({'status': 0, 'msg': 'Your account is not acivated.'}, status=200)
            else:
                    return JsonResponse({'status': 0, 'msg': 'Mobile Number did not match'}, status=200)
        except User.DoesNotExist:
                return JSONResponse({'status': 0, 'msg': 'Authentication Error'}, status=401)
        else:
            return JsonResponse({'msg': 'Mobile Or Password did not match'}, status=401)


class SellerUserRegistrationView(generics.ListAPIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            requestData = serializer.validated_data
            email = requestData['email']
            username = email.split("@")[0]
            password = requestData['password']
            phone_no = requestData['phone_no']
            first_name = requestData['first_name']
            last_name = requestData['last_name']
            p_d=first_name+'_'+password
            account = account_encoder(p_d)
            ## check Email aiiready exist or not
            user = User.objects.filter(email=email,is_deleted=False).count()
            user_no = User.objects.filter(phone_no=phone_no, is_deleted=False).count()
            if user > 0:
                msg = {"Unauthorized error ": ['Email already exists.', ]}
                errors = {'errors': msg}
                return JSONResponse(errors, status=401)
            elif user_no >0:
                msg = {"Unauthorized error ": ['Mobile already exists.', ]}
                errors = {'errors': msg}
                return JSONResponse(errors, status=401)
            else:
                obj = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_no=phone_no,
                    username=username,
                    account=account,
                    is_staff=False,
                    is_superuser=False,
                    is_phone_verified=False,
                    is_email_verified=False,
                    is_active=True,
                    user_type=2
                )
                obj.set_password(password)
                obj.save()
                data = {
                    'status': 1,
                    'id': obj.id,
                    'email': obj.email,
                    'username': obj.username,
                    'message': 'User create successfully'
                }
                return JSONResponse(data, status=200)
        else:
            return JsonResponse({'msg': 'Email Or Password did not match'}, status=400)

class GetAccountView(generics.ListAPIView):
    lookup_field = 'pk'
    def post(self, request, *args, **kwargs):
        phone_no = request.data['phone_no']
        rs = Users.objects.filter(phone_no=phone_no).values('account').distinct()
        account = account_decoder(rs[0]['account'])
        if rs:
            data = {
                'status': 1,
                'error_type': 'email_exist',
                'message': account
            }
            return Response(data)
        else:
            data = {
                'status': 0,
                'error_type': '',
                'message': 'Email Does not Exist',
            }
            return Response(data)

#######################################################################################################
# For Customer
class CheckCustomerEmailView(APIView):

    # serializer_class=User.objects.filter()
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        UserProfile = get_user_model()
        rs = UserProfile.objects.all().filter(email=email, is_deleted=False, user_type=1).first()
        if rs:
            msg = "Email Already linked with another user"
            data = {
                'status': 1,
                'error_type': 'Email Already exist',
                'message': msg
            }
        else:
            data = {
                'status': 0,
                'error_type': '',
                'message': 'Email Does not Exist',
            }
        
        return Response(data)


class CheckCustomerPhoneView(APIView):
    # queryset=''
    # serializer_class=ProfileinfoSerializer
    lookup_field = 'pk'

    def post(self, request, *args, **kwargs):
        phone_no = request.data['phone_no']
        UserProfile = get_user_model()
        count = UserProfile.objects.all().filter(phone_no=phone_no, is_deleted=False, user_type = 1).count()
        if count > 0:
            data = {
                'status': 1,
                'error_type': 'phoneno_exist',
                'message': 'Number is Already Linked Try Different!!',
            }
        else:
            data = {
                'status': 0,
                'error_type': '',
                'message': 'Phone No Does not Exist',
            }
        return Response(data)




###########################################################################################################



class CheckEmailView(APIView):

    lookup_field = 'pk'

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        UserProfile = get_user_model()
        rs = UserProfile.objects.all().filter(email=email, is_deleted="False").first()
        # count = len(rs)
        if rs:
            msg = "Email Already linked with another user"
            data = {
                'status': 1,
                'error_type': 'email_exist',
                'message': msg
            }
            return Response(data)
        else:
            data = {
                'status': 0,
                'error_type': '',
                'message': 'Email Does not Exist',
            }
            return Response(data)


class CheckPhoneView(generics.ListAPIView):
    lookup_field = 'pk'

    def post(self, request, *args, **kwargs):
        phone_no = request.data['phone_no']
        UserProfile = get_user_model()
        count = UserProfile.objects.all().filter(phone_no=phone_no, is_deleted="False").count()
        if count > 0:
            data = {
                'status': 1,
                'error_type': 'phoneno_exist',
                'message': 'Number is Already Linked Try Different!!',
            }
            return Response(data)
        else:
            data = {
                'status': 0,
                'error_type': '',
                'message': 'Phone No Does not Exist',
            }
            return Response(data)

def account_encoder(account):
    account_string_bytes = account.encode("ascii")
    base64_bytes = base64.b64encode(account_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return  base64_string

def account_decoder(account):
    account_string_bytes = account.encode("ascii")
    base64_bytes = base64.b64decode(account_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string