from msilib.schema import Class, SelfReg
from pyexpat import model

from attr import field, fields
from django.test import modify_settings
from .models import  Address, Cart, Coupon, DeliveryCost, Payment,  UserProfile, Orders
from rest_framework import serializers
# from user.models import Users
# from django.contrib.auth import get_user_model

# # User = get_user_model()
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Users
#         fields = ['id', 'username']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'item', 'quantity', 'created_at', 'updated_at']


class DeliveryCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryCost
        fields = ['id', 'status', 'cost_per_delivery', 'cost_per_product', 'fixed_cost', 'created_at', 'updated_at']




# class ItemSerializer(serializers.ModelSerializer):
#    class Meta:
#         model =Item
#         fields='__all__'     


# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= Order
#         fields='__all__'    


# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=OrderItem
#         fields='__all__' 

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields='__all__'

class paymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payment
        fields='__all__'

class UserprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields='__all__'


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model=Coupon
        fields='__all__'

# class RefundSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Refund 
#         fields='__all__'      

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'
        read_only_fields = ('user','status','orderID','userID')

