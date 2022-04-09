from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'category', views.CategoryViewSet)
router.register(r'product', views.ProductViewSet)
router.register(r'Banner', views.BannerViewSet)

urlpatterns = [
    path('', include((router.urls, 'shopping_cart_api.products'))),
    path('count-the-number-of-products/',views.productcountView.as_view()),
]
