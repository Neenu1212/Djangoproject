from django.contrib import admin

# Register your models here.
from django.contrib import admin
from shop.models import  category
from shop.models import  product


admin.site.register(category)
admin.site.register(product)
