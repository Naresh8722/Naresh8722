from django.contrib import admin
from .models import Campaign, Coupon

# admin.site.register(Campaign)
# admin.site.register(Coupon)

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display=['discount_type','discount_rate','discount_amount','min_purchased_items','apply_to','target_product','target_category']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display=['minimum_cart_amount', 'discount_rate',]