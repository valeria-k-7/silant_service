from django.contrib import admin
from .models import MaintenanceType, MaintenanceOrganization, Maintenance

admin.site.register(MaintenanceType)
admin.site.register(MaintenanceOrganization)
admin.site.register(Maintenance)
