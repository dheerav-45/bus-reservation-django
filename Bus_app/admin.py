from django.contrib import admin

from .models import *

admin.site.register(CustomUser)
admin.site.register(Route)
admin.site.register(Bus_Model)
admin.site.register(Bus_BookingModel)
admin.site.register(Review_Model)
admin.site.register(Payment_Model)
