from rest_framework.authentication import TokenAuthentication
# from Grooming.admin import GroomerBookingslotAdmin
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Hygienicpamper, Bugrecue,Happyandshiny,Shinyandbugfree,Groomer, GroomerBookingslot
from .serializers import *
from rest_framework import viewsets

class HygienicpamperViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Hygienicpamper.objects.all()
    serializer_class =  HygienicpamperSerializer


class BugrecueViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes=(IsAuthenticatedOrReadOnly,)
    queryset=Bugrecue.objects.all()
    serializer_class= BugrecueSerializer

class HappyandshinyViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset=Happyandshiny.objects.all()
    serializer_class= HappyandshinySerializer

class ShinyandbugfreeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes=(IsAuthenticatedOrReadOnly,)
    queryset=Shinyandbugfree.objects.all()
    serializer_class= ShinyandbugfreeSerializer




# class BookingView(generics.ListCreateAPIView):
#     permission_classes=(IsAuthenticatedOrReadOnly,)
#     queryset=Booking.objects.all()
#     serializer_class= BookingSerializer       



class GroomerViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes=(IsAuthenticatedOrReadOnly,)
    queryset=Groomer.objects.all()
    serializer_class=GroomerSerializer


class GroomerBookingslotViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes=(IsAuthenticated,)
    queryset=GroomerBookingslot.objects.all()
    serializer_class=GroomerBookingslotSerializer
