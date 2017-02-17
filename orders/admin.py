from django.contrib import admin

from .models import City, Shop, Order\
    # , OrderEntry

admin.site.register(City)
admin.site.register(Shop)

admin.site.register(Order)
# admin.site.register(OrderEntry)
