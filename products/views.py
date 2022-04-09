from itertools import product
from lib2to3.pgen2 import token
from typing import Generic
from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from .models import Category, Product,Banner
from .serializers import BannerSerializer, CategorySerializer, ProductSerializer
# from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework_simplejwt import authentication
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
class CategoryViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'

class ProductViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,)
    queryset = Product.objects.all().order_by('category_id')
    serializer_class = ProductSerializer
    # parser_classes = (FormParser, MultiPartParser)
    filter_backends = [filters.SearchFilter]
    search_fields = '__all__'
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'



class BannerViewSet(viewsets.ModelViewSet):
    # permission_classes=(IsAuthenticated,)
    # Authentication_classes=(TokenAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication,)
    queryset=Banner.objects.all()
    serializer_class=BannerSerializer
    parser_classes = (FormParser, MultiPartParser)
    
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import  status

class productcountView(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request, format=None):
        appointment_doctor_count = Product.objects.filter().count()
        appointment_doctor_count = {'appointment_doctor_count': appointment_doctor_count}
        return Response(status=status.HTTP_200_OK, data={'appointment_doctor_count': appointment_doctor_count})
