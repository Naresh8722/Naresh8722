from django.shortcuts import render, redirect
from rest_framework import serializers, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from .models import AdvancedTraining, BasicTraining, Enquireform
from .serializers import AdvancedTrainingSerializer, BasicTrainingSerializer, EnquireformSerializer


class AdvancedTrainingView(generics.ListCreateAPIView):  
    queryset = AdvancedTraining.objects.all()
    serializer_class =  AdvancedTrainingSerializer


class BasicTrainingView(generics.ListCreateAPIView):
    queryset=BasicTraining.objects.all()
    serializer_class= BasicTrainingSerializer

class EnquireformView(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    queryset=Enquireform.objects.all()
    serializer_class= EnquireformSerializer