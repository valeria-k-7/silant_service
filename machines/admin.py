from django.contrib import admin

from .models import (
    TechniqueModel,
    EngineModel,
    TransmissionModel,
    DriveAxleModel,
    SteeringAxleModel,
    Machine,
)

admin.site.register(TechniqueModel)
admin.site.register(EngineModel)
admin.site.register(TransmissionModel)
admin.site.register(DriveAxleModel)
admin.site.register(SteeringAxleModel)
admin.site.register(Machine)
