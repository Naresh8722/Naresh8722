from django.contrib import admin
from django.db.models import Count
from .models import Cart, Coupon, DeliveryCost, Orders, Payment, UserProfile, Address

# @admin.register(DeliveryCost)
# class DeliveryCostAdmin(admin.ModelAdmin):
#     list_display=['status','cost_per_delivery','cost_per_product','fixed_cost','created_at']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(CartAdmin, self).get_queryset(request)
        return qs.annotate(item_count=Count('item'))

    def item_count(self, inst):
        return inst.item_count 
    
    list_display=['user', 'item','quantity','created_at','get_final_price','item_count']
    list_filter=['user','item','quantity', 'created_at']
    search_fields = ('user','item','created_at')



# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
    
#     list_display=('id','user','get_total','billing_address')
#     list_filter=['user']

# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
    
#     list_display=['id',]
#     list_filter=[]

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display=['id','user','street_address','apartment_address','zip','address_type','default']

admin.site.register(UserProfile)
# admin.site.register(Item)

# admin.site.register(Address)

admin.site.register(Payment)


# admin.site.register(Orders)

# admin.site.register(Coupon)
# admin.site.register(Refund)