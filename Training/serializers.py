from django.db.models import fields
from rest_framework import serializers
from .models import AdvancedTraining, BasicTraining, Enquireform


class AdvancedTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model=AdvancedTraining
        fields='__all__'

class BasicTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model=BasicTraining
        fields='__all__'


class EnquireformSerializer(serializers.ModelSerializer):
    class Meta:
        model=Enquireform
        fields='__all__'
