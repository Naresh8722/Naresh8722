from datetime import date
from rest_framework import viewsets
from rest_framework import  status
# from rest_framework.serializers import Serializer
from rest_framework.views import APIView
# from rest_framework import generics
# from rest_framework_simplejwt import authentication
# from rest_framework import permissions
from rest_framework.response import Response
from .models import Doctor, Appointment
from .serializers import DoctorSerializer,AppoinmentSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

class DoctorViewSet(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes=(IsAuthenticatedOrReadOnly,)
    queryset=Doctor.objects.all()
    serializer_class=DoctorSerializer
    parser_classes = (FormParser, MultiPartParser)


class DoctorcountView(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request, format=None):
        doctor_count = Doctor.objects.count()
        doctor_count = {'doctor_count': doctor_count}
        return Response(status=status.HTTP_200_OK, data={'doctor_count': doctor_count})

        
    

from django_filters.rest_framework import DjangoFilterBackend

class AppointmentViewSet(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes=(IsAuthenticatedOrReadOnly,)
    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,) 
    queryset=Appointment.objects.all()
    serializer_class=AppoinmentSerializer   
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['timeslot','date',]
     


class AppointmentDoctorcountView(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request, format=None):
        appointment_doctor_count = Appointment.objects.count()
        appointment_doctor_count = {'appointment_doctor_count': appointment_doctor_count}
        return Response(status=status.HTTP_200_OK, data={'appointment_doctor_count': appointment_doctor_count})


class AppointmentDoctorcountView(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request, format=None):
        appointment_doctor_count = Appointment.objects.filter().count()
        appointment_doctor_count = {'appointment_doctor_count': appointment_doctor_count}
        return Response(status=status.HTTP_200_OK, data={'appointment_doctor_count': appointment_doctor_count})