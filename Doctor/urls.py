# from django.contrib import admin
# from django.conf.urls import url
# from django.urls import path, include
# # from django.urls import path
# from dj_rest_auth.registration.views import RegisterView, VerifyEmailView,ConfirmEmailView
# from dj_rest_auth.views import LoginView, LogoutView
# from django.conf import settings
# from django.conf.urls.static import static
# from users import views 
# from .views import getPhoneNumberRegistered
# urlpatterns = [
#     #  path('register/', RegisterView.as_view()),
#     #  path('login/', LoginView.as_view()),
#     #  path('logout/', LogoutView.as_view()),

#      path('verify-email/',
#          VerifyEmailView.as_view(), name='rest_verify_email'),
#      path('account-confirm-email/',
#          VerifyEmailView.as_view(), name='account_email_verification_sent'),
#      url(r'^account-confirm-email/(?P<key>[-:\w]+)/$',
#          VerifyEmailView.as_view(), name='account_confirm_email'),
#      url(r'account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
#     #  path('customer-Loginn/',views.getPhoneNumberRegistered),
#      path('emp', views.emp),  
#      path('show',views.show),  
#      path('edit/<int:id>', views.edit),  
#      path('update/<int:id>', views.update),  
#      path('delete/<int:id>', views.destroy),

#      path('cart', views.addcart),

#     path('home/', views.home),
#     path('signup/', views.signup),
#     path('signin/', views.signin),
#     path('signout/', views.signout),
#     # path('rest-auth/google/', views.GoogleLogin.as_view(), name='redirect')    
     
      
# ]
# if settings.DEBUG:
#     urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# from django.conf import settings
# from django.urls import path, include
# # from Doctor import views
# from django.conf.urls.static import static

# from Doctor.views import DoctorView,AppointmentView,DetailsDoctor


# urlpatterns =[

#     path('api/doctor/', DoctorView.as_view(), name='doctor'),
#     path('api/appointment/', AppointmentView.as_view(), name='appointment'),
#     path('doctor/<int:pk>/', DetailsDoctor.as_view(), name='doctor'),
# ]
# if settings.DEBUG:
#     urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'doctor', views.DoctorViewSet)
router.register(r'appointment', views.AppointmentViewSet)

urlpatterns = [
    path('', include((router.urls, 'Doctor'))),
    path("doctorcount/", views.DoctorcountView.as_view()),
    path('appointmentcount/',views.AppointmentDoctorcountView.as_view()),
]



 