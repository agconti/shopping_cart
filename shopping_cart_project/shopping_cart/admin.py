#admin.py
from django.contrib import admin
from shopping_cart.models import Merchant, Store, Item, Order

admin.site.register(Merchant)
admin.site.register(Store)
admin.site.register(Item)
admin.site.register(Order)