from .models import Category, Product, Banner
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'parent_category_id', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.FileField(max_length=100, use_url=True)
    class Meta:
        model = Product
        fields = ['id','seller','user', 'title','name','category','image','price','discount','quantity','stock','available','description','created_at', 'updated_at']
    def create(self, validated_data):
        image=validated_data.pop('image')
        for img in image:
            image=Product.objects.create(image=img,**validated_data)
        return image
    

class BannerSerializer(serializers.ModelSerializer):
    image1 = serializers.ImageField(max_length=100, use_url=True)
    image2 = serializers.ImageField(max_length=100, use_url=True)
    image3 = serializers.ImageField(max_length=100, use_url=True)
    class Meta:
        model=Banner
        fields=["image1","image2","image3"]
    # def create(self, validated_data):
    #     image=validated_data.pop('image1')
    #     for img in image:
    #         image=Banner.objects.create(image=img,**validated_data)
    #     return image

        

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Category, Product
from drf_extra_fields.fields import Base64ImageField


class ProductDetailSerializer(serializers.ModelSerializer):
    seller = serializers.SlugRelatedField(slug_field="username", queryset=User.objects)
    category = serializers.SerializerMethodField()
    image = Base64ImageField()

    def get_category(self, obj):
        return obj.category.name

    class Meta:
        model = Product
        exclude = "modified"