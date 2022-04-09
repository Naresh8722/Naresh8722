# from django.db.models import fields
from rest_framework import serializers
from .models import Hygienicpamper,Bugrecue,Happyandshiny,Shinyandbugfree,  Groomer, GroomerBookingslot


class HygienicpamperSerializer(serializers.ModelSerializer):
    class Meta:
        model=Hygienicpamper
        fields='__all__'

class BugrecueSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bugrecue
        fields='__all__'


class HappyandshinySerializer(serializers.ModelSerializer):
    class Meta:
        model=Happyandshiny
        fields='__all__'


class ShinyandbugfreeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Shinyandbugfree
        fields='__all__'


# class BookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Booking
#         fields='__all__'


class GroomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Groomer
        fields='__all__'


class GroomerBookingslotSerializer(serializers.ModelSerializer):
    class Meta:
        model=GroomerBookingslot
        fields='__all__'        


