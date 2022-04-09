# from django.conf import settings
# from django.urls import path, include
# # from Doctor import views
# from django.conf.urls.static import static

# # from petishh.Grooming.admin import GroomerAdmin

# from .views import HygienicpamperView,BugrecueView,HappyandshinyView,ShinyandbugfreeView, GroomerListView, GroomerBookingslotListView


# urlpatterns =[

#     path('hygienic/', HygienicpamperView.as_view(), name='hygienic'),
#     path('bugrecue/', BugrecueView.as_view(), name='bugrecue'),
#     path('happyandshiny/', HappyandshinyView.as_view(), name='Happy and Shiny'),
#     path('shinyandbugfree/',ShinyandbugfreeView.as_view(), name='shiny and bugfree'),
#     # path('booking/', BookingView.as_view(), name='booking'),
#     path('groomerdetails/', GroomerListView.as_view(), name='groomer add'),
#     path('groomerbooking/',GroomerBookingslotListView.as_view(), name='groomerbookingslot')

# ]
# if settings.DEBUG:
#     urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf import settings

from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'HygienicpamperViewSet', views.HygienicpamperViewSet)
router.register(r'BugrecueViewSet', views.BugrecueViewSet)
router.register(r'HappyandshinyViewSet', views.HappyandshinyViewSet)
router.register(r'ShinyandbugfreeViewSet', views.ShinyandbugfreeViewSet)
router.register(r'GroomerViewSet', views.GroomerViewSet)
router.register(r'GroomerBookingslotViewSet', views.GroomerBookingslotViewSet)


urlpatterns = [
    path('', include((router.urls, 'Grooming'))),
]


# if settings.DEBUG:
#     urlpatterns+=static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS)
#     urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)