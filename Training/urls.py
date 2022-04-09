from django.conf import settings
from django.urls import path, include
# from Doctor import views
from django.conf.urls.static import static

from .views import AdvancedTrainingView, BasicTrainingView, EnquireformView


urlpatterns =[

    path('advanced-training/',AdvancedTrainingView.as_view(), name='advanced'),
    path('basic-training/', BasicTrainingView.as_view(), name='basic'),
    path('enqurirefrom/', EnquireformView.as_view(), name='enquire'),
]
if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)