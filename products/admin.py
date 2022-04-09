from email.mime import image
from django.contrib import admin
# from django.contrib.admin.filters import ListFilter
from .models import Category, Product,Banner

# admin.site.register(Category)
# admin.site.register(Product)
# admin.site.register(Banner)
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display=['id','image_tag1','image_tag2','image_tag3']
# class ProductInstanceInline(admin.TabularInline):
#     model = Product
@admin.register(Product)
class productAdmin(admin.ModelAdmin):
    # save_on_top=True
    # view_on_site = True
    search_fields = ['name','price',]
    list_display=['id','image_tag','category','name','price','available',]
    list_filter=('id','title','category','price','name','available',)
    # inlines = [ProductInstanceInline]
    
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['title','parent_category_id']
    list_filter=('title',)    


# class ProductAdmin(admin.ModelAdmin):
#     search_fields = ['titel','price']
#     def changelist_view(self, request, extra_context=None):
#         # Add extra context data to pass to change list template
#         extra_context = extra_context or {}
#         extra_context['my_store_data'] = {'onsale':['product_name','category']}
#         # Execute default logic from parent class changelist_view()
#         return super(ProductAdmin, self).changelist_view(
#             request, extra_context=extra_context
#         )
#     def delete_view(self, request, object_id, extra_context=None):
#         # Add custom audit logic here
#         # Execute default logic from parent class delete_view()
#         return super(ProductAdmin, self).delete_view(
#             request, object_id, extra_context=extra_context
#         )
# admin.site.register(Product, ProductAdmin)      