from django.contrib import admin
from .models import CustomUser,VehicleOwnerDocument,IndustrialOwnerDocument

admin.site.register(CustomUser)
admin.site.register(VehicleOwnerDocument)
admin.site.register(IndustrialOwnerDocument)