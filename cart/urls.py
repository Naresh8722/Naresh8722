from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'Cart', views.CartViewSet)
router.register(r'Delivery-cost', views.DeliveryCostViewSet)
# router.register(r'Items', views.ItemViewSet)
router.register(r'Userprofile', views.UserprofileViewSet)
# router.register(r'Order',views.OrderViewSet)
# router.register(r'OrderItems',views.OrderItemsViewSet)
router.register(r'OrderAddres',views.AddressViewSet)
router.register(r'Payment',views.PaymentViewSet)
router.register(r'OrderStatusView', views.OrderStatusView)

urlpatterns = [
    path('', include((router.urls, 'shopping_cart_api.cart'))),
    path("cart/count/", views.cartcountView.as_view())
]

