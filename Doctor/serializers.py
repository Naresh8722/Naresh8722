from django.db.models import fields
from rest_framework import serializers
from .models import Doctor, Appointment


class DoctorSerializer(serializers.ModelSerializer):
    image = serializers.FileField(max_length=100, use_url=True)
    class Meta:
        model=Doctor
        fields=['id','first_name','middle_name','last_name','image','specialty']
    def create(self, validated_data):
        image=validated_data.pop('image')
        for img in image:
            image=Doctor.objects.create(image=img,**validated_data)
        return image        

class AppoinmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Appointment
        fields='__all__'


