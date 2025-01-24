from django.contrib import admin
from .models import *



admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(DeliveryAddress)
admin.site.register(UserProfile)
admin.site.register(PaymentInfo)