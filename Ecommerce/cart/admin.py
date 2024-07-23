from django.contrib import admin

# Register your models here.
from cart.models import cart
from cart.models import ordertable
from cart.models import Payment


admin.site.register(cart)
admin.site.register(ordertable)
admin.site.register(Payment)