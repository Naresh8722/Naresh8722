"""petishh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from allauth.account.views import confirm_email
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
# from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
# from user.views import RegistrationappAPIView, loginview,CustomAuthToken

from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView



from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.views.static import serve

schema_view = get_schema_view(
    openapi.Info(
        title="PETTISH API",
        default_version='v1',
        description="Test description",
        terms_of_service='petishh.herokuapp.com',
        contact=openapi.Contact(email="naresh11021@gmail.com"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [

    # url(r'^', include(router.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('admin/', admin.site.urls),
        # path('admin/password_reset/',auth_views.PasswordResetView.as_view(),name='admin_password_reset'),
        # path('admin/password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done', ),
        # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm',),
        # path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete',),
        # path('', include('events.urls')),          
    path('user/', include('user.urls')),
    path('socialapp/', include('socialauthapp.urls')),
    # path('api/otp/', include('custom_users.urls')),
    path('api-auth/', include('rest_framework.urls')),
    # path('auth/register/user/', RegistrationappAPIView.as_view(), name='authregister'),
    # path('user/login/', loginview.as_view(), name='login views'),
    # path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path('Cart/', include('cart.urls')),
    path('Discounts/', include('discounts.urls')),
    path('Products/', include('products.urls')),
    path('Doctor/', include('Doctor.urls')),
    path('Training/', include('Training.urls')),
    path('Grooming/', include('Grooming.urls')),
    # path('orders/', include('order.urls')),
    # path('dj-rest-auth/', include('dj_rest_auth.urls')), 
    # url(r'^dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    # url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    # path('token-auth/login/', CustomAuthToken.as_view()),
    url(r'^accounts/', include('allauth.urls')),
    # url(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'), 
    path('password-reset/',PasswordResetView.as_view()),
    path('password-reset-confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(), name='password_reset_confirm'), 


    # url(r'api/auth/', include('knox.urls')),
    # path('rest_framework_simplejwt-token/',include('rest_framework_simplejwt.urls')),    
    path('', schema_view.with_ui('swagger',
                                 cache_timeout=0), name='schema-swagger-ui'),

    path('api/api.json/', schema_view.without_ui(cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
                                       cache_timeout=0), name='schema-redoc'),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),                                    
]
# if settings.DEBUG:
urlpatterns +=static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS)
# urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

























































































































































































































































































































































































































































































































































































































































































































































































































