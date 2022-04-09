from django.db.models import query
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.serializers import Serializer
from user.serializers import *
from django.utils import timezone
import base64
from rest_framework.permissions import IsAuthenticated  
from slugify import slugify
import random



class JSONResponse(HttpResponse):
    """ An HttpResponse that renders its content into JSON. """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class SellerUserLoginView(generics.ListAPIView):
    queryset = ""
    erializer_class= LoginSerializer
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            requestData = serializer.validated_data
            mobile = requestData['phone_no']
            password = requestData['password']
            User = get_user_model()
            try:  ## Check user Number Exist
                user = User.objects.filter(phone_no=mobile,user_type=2, is_deleted=False, is_blocked=False, status=True).first()
                if user:
                    print(password)
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
                                        'is_shop_verified': user.is_shop_verified,
                                        'is_submitted':user.is_submitted,
                                        'last_login': user.last_login
                                    }
                                    return JsonResponse({'status': 0, 'msg': 'Login Successfull'}, status=200)
                                else:
                                    return JsonResponse({'status': 0, 'msg': 'Your account is not activated.'}, status=200)
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
                    return JsonResponse({'status': 0, 'msg': 'Account is disabled by Admin, Please write to petishh.com'}, status=200)
            except User.DoesNotExist:
                return JsonResponse({'status': 0, 'msg': 'Authentication Error'}, status=401)
        else:
            return JsonResponse({'msg': 'Invalid'}, status=401)


class SellerUserLoginOtpView(generics.ListAPIView):
    queryset=""
    serializer_class=LoginOtpSerializer
    def post(self, request):
        phone_no = request.data.get('phone_no')
        User = get_user_model()
        try:  ## Check user Number Exist
            user = User.objects.filter(phone_no=phone_no, is_deleted=False, is_blocked=False).first()
            if user:
                if user.is_active:  ## Check user active or not
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
                         'is_shop_verified': user.is_shop_verified,
                        'is_submitted':user.is_submitted,
                        'is_staff': user.is_staff,
                        'last_login': user.last_login,
                    }
                    # print(serialize_userdata)
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
    queryset=''
    serializer_class=SignupSellerSerializer
    def post(self, request):
        serializer = SignupSellerSerializer(data=request.data)
        if serializer.is_valid():           
            print("started validation")
            requestData = serializer.validated_data
            print(requestData)
            # name = requestData['name']
            # nme = name.split()


            # if len(name) > 2 or len(name) ==2 :
            #     fname = nme[0]
            #     lname = nme[-1]

            # else:
            #     fname = nme
            #     lname = ''

            # first_name = fname
            # last_name = lname

            first_name=requestData['first_name']
            last_name=requestData['last_name']
            email = requestData['email']
            phone_no = requestData['phone_no']

            shop_name = requestData['shop_name']
            shop_city = requestData['shop_city']
            state = requestData['state']
            password = requestData['password']
            refererid = requestData['referel_code']

            referelcode ='home'+str(random.randint(10000000, 99999999))
            wallet=0
            p_d= first_name+'_'+password
            account = account_encoder(p_d)
            username = email.split("@")[0]

            ## check Email aiiready exist or not
            user = Users.objects.filter(email=email,is_deleted=False).count()
            user_no = Users.objects.filter(phone_no=phone_no, is_deleted=False).count()
            usernm = Users.objects.filter(username=username,is_deleted=False).count()
            print("=================",user,usernm,user_no)
            if usernm>0:
                username=username+str(random.randint(1000, 9999))
            if user > 0:
                msg = {"Error ": ['Email already Registered....', ]}
                errors = {'errors': msg}
                return JSONResponse(errors, status=401)
            elif user_no >0:
                msg = {"Error ": ['Mobile Already Registered....', ]}
                errors = {'errors': msg}
                return JSONResponse(errors, status=401)
                # if email != user.email:
                #     try:
                #         subject = 'Email error '
                #         message = 'Email enter incorrectly please check'
                #         recepient = str(sub['Email'].value())
                #         send_mail(subject, 
                #             message, user.email, [EMAIL_HOST_USER], fail_silently = False)
                #         return JsonResponse({'status': 1, 'msg': 'Email sent successfully'}, status=200)
                #     except:
            else:
                obj = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    
                    email=email,
                    phone_no=phone_no,
                    username=username,
                    account=account,
                    refererid = refererid,
                    referelcode = referelcode,
                    shop_name = shop_name,
                    shop_city = shop_city,
                    state = state,
                    wallet=wallet,
                    is_staff=False,
                    is_superuser=False,
                    is_phone_verified=False,
                    is_email_verified=False,
                    is_active=True,
                    user_type=2,
                    status=True
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



class SSSellerUserRegistrationView(generics.ListAPIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():           
            print("started validation")
            requestData = serializer.validated_data
            print(requestData)
            email = requestData['email']
            password = requestData['password']
            phone_no = requestData['phone_no']
            first_name = requestData['first_name']
            last_name = requestData['last_name'] 
            refererid = request.data['referelcode']
            referelcode ='home'+str(random.randint(10000000, 99999999))
            wallet=0
            p_d=first_name+'_'+password
            account = account_encoder(p_d)
            username = email.split("@")[0]

            ## check Email aiiready exist or not
            # if email != user.email:
            #     try:
            #         subject = 'Email verification failed'
            #         message = 'Please check your email id as you mentioned your email id in-correctly'
            #         recepient = str(sub['Email'].value())
            #         send_mail(subject, 
            #             message, EMAIL_HOST_USER, [user.email], fail_silently = False)
            #         return JsonResponse({'status': 1, 'msg': 'Email sent successfully'}, status=200)
            #     except:
            #         # return JsonResponse({'status': 4, 'msg': 'Entered ',"email":user.email}, status=202)
            
            user = User.objects.filter(email=email,is_deleted=False).count()

            user_no = User.objects.filter(phone_no=phone_no, is_deleted=False).count()
            usernm = User.objects.filter(username=username,is_deleted=False).count()  
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
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_no=phone_no,
                    username=username,
                    account=account,
                    refererid = refererid,
                    referelcode = referelcode,
                    wallet=wallet,
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

class CheckAdminEmailView(generics.ListAPIView):
    lookup_field = 'pk'

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        UserProfile = get_user_model()
        rs = UserProfile.objects.all().filter(email=email, is_superuser=True, is_deleted="False").first()
        # count = len(rs)
        if rs:
            msg = "Already Registered"
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
                'message': 'No Admin Access',
            }
            return Response(data)



class CheckEmailView(generics.ListAPIView):
    lookup_field = 'pk'

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        UserProfile = get_user_model()
    
        rs = UserProfile.objects.all().filter(email=email, is_deleted="False",user_type=2).first()
        
# count = len(rs)
        if rs:
            
            msg = "Already Registered"
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
                'message': 'Email Not Registered',
            }
            return Response(data)


class CheckPhoneView(generics.ListAPIView):
    lookup_field = 'pk'

    def post(self, request, *args, **kwargs):
        phone_no = request.data['phone_no']
        UserProfile = get_user_model()
        count = UserProfile.objects.all().filter(phone_no=phone_no,user_type=2).count()
        if count > 0:
            data = {
                'status': 1,
                'error_type': 'phoneno_exist',
                'message': 'Already Registered',
            }
            return Response(data)
        else:
            data = {
                'status': 0,
                'error_type': '',
                'message': 'Phone Number not Registered',
            }
            return Response(data)



# class ChangePasswordView(generics.UpdateAPIView):
#     serializer_class = ChangePasswordSerializer
#     model = User
#     permission_classes = (IsAuthenticated,)
#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)
#         print(request.data)

#         if serializer.is_valid():
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             response = {
#                 'status': 'success',
#                 'code': 200,
#                 'message': 'Password updated successfully',
#                 'data': []
#             }
#             return Response(response)
#         return Response(serializer.errors, status=400)

class ChangePasswordView(generics.UpdateAPIView):
    def put(self, request, format=None):
        response_data = {}
        user = request.user
        user_id = user.id
        requestdata = request.data
        rs = User.objects.filter(phone_no=requestdata['mobile'], is_active=True, is_blocked=False, is_deleted=False)
        if rs:
            for i in rs:
                first_name = i.first_name
            p_d=first_name+'_'+requestdata['new_password']
            account = account_encoder(p_d)
            obj = User.objects.filter(phone_no=requestdata['mobile']).update(
                account=account
            )
            new = User.objects.get(phone_no = requestdata['mobile'])
            new.set_password(requestdata['new_password'])
            new.save()
            response_data['status'] = 1
            response_data['massage'] = "Password Updated Successfully"
            response_data['user_id'] = user_id
            return Response(response_data, status=200)
        else:
            response_data['status'] = 0
            response_data['massage'] = "User not found"
            response_data['user_id'] = user_id
            return Response(response_data, status=200)


class ChangeAdminPasswordView(generics.UpdateAPIView):
    def put(self, request, format=None):
        response_data = {}
        user = request.user
        user_id = user.id
        requestdata = request.data
        rs = User.objects.filter(email=requestdata['email'], is_active=True, is_superuser=True, is_blocked=False, is_deleted=False)
        if rs:
            for i in rs:
                first_name = i.first_name
            p_d=first_name+'_'+requestdata['new_password']
            account = account_encoder(p_d)
            obj = User.objects.filter(email=requestdata['email']).update(
                account=account
            )
            new = User.objects.get(email = requestdata['email'])
            new.set_password(requestdata['new_password'])
            new.save()
            response_data['status'] = 1
            response_data['massage'] = "Password Updated Successfully"
            response_data['user_id'] = user_id
            return Response(response_data, status=200)
        else:
            response_data['status'] = 0
            response_data['massage'] = "User not found"
            response_data['user_id'] = user_id
            return Response(response_data, status=200)

    # def update(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     serializer = self.get_serializer(data=request.data)

    #     if serializer.is_valid():
    #         self.object.set_password(serializer.data.get("new_password"))
    #         self.object.save()
    #         response = {
    #             'status': 1,
    #             'code': 200,
    #             'message': 'Password updated successfully',
    #             'data': []
    #         }
    #     else:
    #         response ={
    #             'status': 0,
    #             'code' : 400,
    #         }
    #     return Response(serializer.errors, status=200)

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