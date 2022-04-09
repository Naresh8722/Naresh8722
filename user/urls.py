from user.serializers import ResetPasswordEmailRequestSerializer
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken import views as restview
from user.webservice import customer_profile_view
# from user.webservice import seller_signin_signup_view, mobile_otp_view, email_view, customer_profile_view, notification_view, customer_sigin_view
from django.contrib.auth import views as auth_views
from .views import  VerifyEmail, RegistersView, LoginAPIView, LogoutAPIView, UsercountView
urlpatterns = [
    url(r'^register/$',RegistersView.as_view(), name='register'),
    url(r'^email-verify/$', VerifyEmail.as_view(),name='email-verify'),
    url(r'^login/$', LoginAPIView.as_view(), name="login"),
    url(r'^logout/$', LogoutAPIView.as_view(), name="logout"),
    url(r'^no_user_db/$',UsercountView.as_view(), name="no_user_count_db"),
    #######################################################################################################################
                                                        ## Customer APIs ##
  #   #######################################################################################################################
  #   #### Register
    # url(r'^customer-Registration/$',customer_sigin_view.CustomerRegistrationView.as_view(), name=''),
  #   #### verify email and phone #####
  #   url(r'^check-customer-email/$',customer_sigin_view.CheckCustomerEmailView.as_view(),name='check-customer-email'),
  #   url(r'^check-customer-phone/$',customer_sigin_view.CheckCustomerPhoneView.as_view(),name='check-customer-phone'),
  #   ##### Send and verify OTP #####
  #   url(r'^send-otp-cust/$',mobile_otp_view.MobileDetailsViewCustomer.as_view(),name='send-cust-otp'),
  #   url(r'^send-mail-cust/$', mobile_otp_view.EmailDetailsViewCustomer.as_view(),name='send-mail-cust'),
  #   url(r'^check-otp-cust/$',mobile_otp_view.OtpVerificationViewCustomer.as_view(),name='check-otp-cust'),
  #   url(r'^check-otp-mail-cust/$',mobile_otp_view.EmailOtpVerificationViewCustomer.as_view(),name='check-mail-cust'),
  #   ##### Login
    # url(r'^customer-Login/$',customer_sigin_view.CustomerLoginView.as_view(), name='customer-Login'),
  #   url(r'^customer-OtpView/$',customer_sigin_view.CustomerLoginOtpView.as_view(), name='customer-OtpView'),
  #   ##### Customer Login Register Management  ####
    url(r'^customer-info/$', customer_profile_view.CustomerProfileView.as_view(),name='customer-info'),
  #   #### Get And Update Customer Profile   ####
    # url(r'^get-cutomerProfile/$', customer_profile_view.CustomerProfileView.as_view(),name='get-customerProfile'),

  #   ##### User Management #####
    # url(r'^seller-login/$', seller_signin_signup_view.SellerUserLoginView.as_view(), name='seller-login'),
    # url(r'^seller-registration/$', seller_signin_signup_view.SellerUserRegistrationView.as_view(), name='seller-registration'),
    # url(r'vendor-loginOtp/',seller_signin_signup_view.SellerUserLoginOtpView.as_view(), name='vendor-loginOtp'),
    # url(r'login-send-otp/',mobile_otp_view.SellerUserLoginOtpView.as_view(), name='login-send-otp'),
    # url(r'^get-account/',seller_signin_signup_view.GetAccountView.as_view(), name='get-account'),

    

  #   ### Email Notification ####
    # url(r'^send-mail/$', mobile_otp_view.EmailDetailsView.as_view(),name='send-mail'),
  # #  url(r'^sendconfirmmail/$', mobile_otp_view.send_conf,name='sendconfirmmail'),
    
  #   url(r'^change-mail/$', mobile_otp_view.ChangeEmailAddress.as_view(),name='change-mail'),

  #   #### rest Password   ####
  #   url(r'^change-password/$', seller_signin_signup_view.ChangePasswordView.as_view(), name='change-password'),
  #   url(r'^change-admin-password/$', seller_signin_signup_view.ChangeAdminPasswordView.as_view(), name='change-admin-password'),
  #   # url(r'^update-password/$', mobile_otp_view.UpdatePassword.as_view(),name='update-password'),

  #   url(r'^check-admin-email/$',seller_signin_signup_view.CheckAdminEmailView.as_view(),name='check-admin-email'),

  #   #### Check Mail ######
  #   url(r'^check-email/$',seller_signin_signup_view.CheckEmailView.as_view(),name='check-email'),
  #   url(r'^check-phone/$',seller_signin_signup_view.CheckPhoneView.as_view(),name='check-phone'),

  #   ##### Send and verify OTP for vendor #######
  #   url(r'^send-otp/$',mobile_otp_view.MobileDetailsView.as_view(),name='send-otp'),
  #   url(r'^check-otp/$',mobile_otp_view.OtpVerificationView.as_view(),name='check-otp'),
    
  #   ####  Verify Mail 
  #   url(r'^check-mail/$',mobile_otp_view.EmailOtpVerificationView.as_view(),name='check-mail'),

  #   url(r'^verifyChange-mail/$',mobile_otp_view.EmailChangeVerificationView.as_view(),name='verifyChange-mail'),

  #   url(r'^change-number-otp/$',mobile_otp_view.ChangeNumberOtp.as_view(),name='change-number-otp'),

  #   url(r'^verifyChange-number/$',mobile_otp_view.NumberChangeVerificationView.as_view(),name='verifyChange-mail'),

  #   url(r'^verifySec-number/$',mobile_otp_view.VerifySecondaryNumber.as_view(),name='verifySec-number'),


  #   ######   Firebase Device  ###
    # url(r'^device-list/$', notification_view.FcmDeviceView.as_view(),name='device-list'),
  #   url(r'^send-notification/$', notification_view.FcmSaveNotification.as_view(),name='send-notification'),
  #   url(r'^oauth/login/$', SocialLoginView.as_view()),
    

    
    # url(r'^social_sign_up/$', views.SocialSignUp.as_view(), name="social_sign_up"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)