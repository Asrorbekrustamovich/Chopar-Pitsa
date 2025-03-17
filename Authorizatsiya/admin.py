from django.contrib import admin
from .models import User, City, Delivery_type, Adress_for_delivery, Contacts, filials
admin.site.register(User)
admin.site.register(City)
admin.site.register(Delivery_type)
admin.site.register(Adress_for_delivery)
admin.site.register(Contacts)
admin.site.register(filials)
