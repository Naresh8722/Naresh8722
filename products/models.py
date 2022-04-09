from django.db import models
from django.db.models.fields.files import ImageField
from rest_framework.routers import flatten
from user.models import Users
from django.conf import settings
import decimal
from django.contrib.auth import get_user_model
from django.utils.html import mark_safe

User = get_user_model()
class Banner(models.Model):
    image1=models.ImageField()
    image2=models.ImageField()
    image3=models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __image__(self):
        return "{}-{}-{}".format(self.image1,
                             self.image2,
                             self.image3)
    def image_tag1(self):
        return mark_safe('<img src="%s" width="40" height="40" />' % (self.image1.url))

    image_tag1.short_description = 'Image'
    image_tag1.allow=True 

    def image_tag2(self):
        return mark_safe('<img src="%s" width="40" height="40" />' % (self.image2.url))

    image_tag2.short_description = 'Image'
    image_tag2.allow=True     

    def image_tag3(self):
        return mark_safe('<img src="%s" width="40" height="40" />' % (self.image3.url))

    image_tag3.short_description = 'Image'
    image_tag3.allow=True                               

class Category(models.Model):
    title = models.CharField(max_length=255, null=False)
    parent_category_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} - {} - {}".format(self.title,
                                          self.parent_category_id,
                                          self.created_at,
                                          self.updated_at)


class Product(models.Model):
    seller = models.ForeignKey(User, related_name="user_product", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_id')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255,  null=False)
    name=models.CharField(max_length=100,default="", null=False)
    # slug = models.SlugField(max_length=200, db_index=True)
    image = models.FileField(default='', null=True, upload_to='product_pics')
    quantity = models.DecimalField(max_digits=10,  decimal_places=2)
    price = models.DecimalField(max_digits=10,  decimal_places=2)
    discount = models.DecimalField(max_digits=10,  decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     if self.image:
    #         self.image = get_thumbnail(self.image, '500x600', quality=99, format='JPEG')
    #     super(Product, self).save(*args, **kwargs)
    
    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.seller,
                                               self.user,
                                               self.category,
                                               self.title,                                              
                                               self.price,
                                               self.discount,
                                               self.image,
                                               self.created_at,
                                               self.updated_at)
    def image_tag(self):
        return mark_safe('<img src="%s" width="40" height="40" />' % (self.image.url))

    image_tag.short_description = 'Image'
    image_tag.allow=True



# class Product(models.Model):
#     category = models.ForeignKey(Category, related_name='products')
#     name = models.CharField(max_length=200, db_index=True)
#     slug = models.SlugField(max_length=200, db_index=True)
#     image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
#     description = models.TextField(blank=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     stock = models.PositiveIntegerField()
#     available = models.BooleanField(default=True)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ('name',)
#         index_together = (('id', 'slug'),)

#     def __str__(self):
#         return self.name