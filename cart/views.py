from rest_framework import viewsets, status,permissions
from rest_framework_simplejwt import authentication
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import  Cart, DeliveryCost
from .serializers import CartSerializer, DeliveryCostSerializer
from .helpers import CartHelper
from user.serializers import *
from  .serializers import *
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = Users.objects.all().order_by('id')
#     serializer_class = UserSerializer


class CartViewSet(viewsets.ModelViewSet):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication,)
    queryset = Cart.objects.all().order_by('id')
    serializer_class = CartSerializer

    @action(methods=['get'], detail=False, url_path='checkout/(?P<userId>[^/.]+)', url_name='checkout')
    def checkout(self, request, *args, **kwargs):
        user = request.user
        user_id = user.id
        rs = User.objects.filter(
            id=user_id, is_active=True, is_blocked=False, is_deleted=False)
        try:
            user = User.objects.get(pk=int(kwargs.get('userId')))
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'Error': str(e)})

        cart_helper = CartHelper(user)
        checkout_details = cart_helper.prepare_cart_for_checkout()

        if not checkout_details:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'error': 'Cart of user is empty.'})

        return Response(status=status.HTTP_200_OK, data={'checkout_details': checkout_details})


class DeliveryCostViewSet(viewsets.ModelViewSet):
    queryset = DeliveryCost.objects.all().order_by('id')
    serializer_class = DeliveryCostSerializer

# class ItemViewSet(viewsets.ModelViewSet):
#     queryset= Item.objects.all().order_by('id')
#     serializer_class= ItemSerializer

# class OrderViewSet(viewsets.ModelViewSet):
#     queryset= Order.objects.all().order_by('id')
#     serializer_class=OrderSerializer


# class OrderItemsViewSet(viewsets.ModelViewSet):
#     queryset=OrderItem.objects.all()
#     serializer_class=OrderItemSerializer
#     @action(methods=['get'], detail=False, url_path='checkout/(?P<userId>[^/.]+)', url_name='checkout')
#     def checkout(self, request, *args, **kwargs):
#         user = request.user
#         user_id = user.id
#         rs = User.objects.filter(
#             id=user_id, is_active=True, is_blocked=False, is_deleted=False)
#         try:
#             user = User.objects.get(pk=int(kwargs.get('userId')))
#         except Exception as e:
#             return Response(status=status.HTTP_404_NOT_FOUND,
#                             data={'Error': str(e)})

#         cart_helper = CartHelper(user)
#         checkout_details = cart_helper.prepare_cart_for_checkout()

#         if not checkout_details:
#             return Response(status=status.HTTP_404_NOT_FOUND,
#                             data={'error': 'Cart of user is empty.'})

#         return Response(status=status.HTTP_200_OK, data={'checkout_details': checkout_details})

class AddressViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication,)
    queryset=Address.objects.all()
    serializer_class=AddressSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication,)   
    queryset=Payment.objects.all()
    serializer_class=paymentSerializer 

class UserprofileViewSet(viewsets.ModelViewSet):
    queryset=UserProfile.objects.all()
    serializer_class=UserprofileSerializer

class CouponViewSet(viewsets.ModelViewSet):
    queryset=Coupon.objects.all()
    serializer_class=CouponSerializer

# class RefundViewSet(viewsets.ModelViewSet):
#     queryset= Refund.objects.all()
#     serializer_class=RefundSerializer

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
class cartcountView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication,)
    queryset=User.objects.filter()
    renderer_classes = [JSONRenderer]
    def get(self, request, format=None):
        cart_count = Cart.objects.filter().count()
        cart_count = {'cart_count': cart_count}
        return Response(status=status.HTTP_200_OK, data={'cart_count': cart_count})


# after checkout oderstatus
from  .models import Orders
from .serializers import OrdersSerializer
from rest_framework import viewsets
class OrderStatusView(viewsets.ModelViewSet):
    serializer_class = OrdersSerializer
    queryset = Orders.objects.all()
    # permission_classes = [AllowAny,]
    def post(self, request):
        data = request.data
        payment_id = data['id']
        payment = mollie_client.payments.get(payment_id)
        orders = self.get_queryset().filter(orderID=payment_id)
        if not orders:
           return Response(status=status.HTTP_400_BAD_REQUEST)
        orders.update(status=payment.status)
        return Response(status=status.HTTP_200_OK, data=payment.status)