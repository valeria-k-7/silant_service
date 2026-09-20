from django.urls import path

from .views import (
    DriveAxleModelCreate,
    DriveAxleModelList,
    DriveAxleModelUpdate,
    EngineModelCreate,
    EngineModelList,
    EngineModelUpdate,
    MachineCreate,
    MachineDetail,
    MachineUpdate,
    SteeringAxleModelCreate,
    SteeringAxleModelList,
    SteeringAxleModelUpdate,
    TechniqueModelCreate,
    TechniqueModelList,
    TechniqueModelUpdate,
    TransmissionModelCreate,
    TransmissionModelList,
    TransmissionModelUpdate,
    machine_list,
)


app_name = 'machines'

urlpatterns = [
    path('', machine_list, name='list'),
    path('create/', MachineCreate.as_view(), name='create'),
    path('<int:pk>/', MachineDetail.as_view(), name='detail'),
    path('<int:pk>/update/', MachineUpdate.as_view(), name='update'),

    path(
        'references/technique-models/',
        TechniqueModelList.as_view(),
        name='technique_model_list',
    ),
    path(
        'references/technique-models/create/',
        TechniqueModelCreate.as_view(),
        name='technique_model_create',
    ),
    path(
        'references/technique-models/<int:pk>/update/',
        TechniqueModelUpdate.as_view(),
        name='technique_model_update',
    ),

    path(
        'references/engine-models/',
        EngineModelList.as_view(),
        name='engine_model_list',
    ),
    path(
        'references/engine-models/create/',
        EngineModelCreate.as_view(),
        name='engine_model_create',
    ),
    path(
        'references/engine-models/<int:pk>/update/',
        EngineModelUpdate.as_view(),
        name='engine_model_update',
    ),

    path(
        'references/transmission-models/',
        TransmissionModelList.as_view(),
        name='transmission_model_list',
    ),
    path(
        'references/transmission-models/create/',
        TransmissionModelCreate.as_view(),
        name='transmission_model_create',
    ),
    path(
        'references/transmission-models/<int:pk>/update/',
        TransmissionModelUpdate.as_view(),
        name='transmission_model_update',
    ),

    path(
        'references/drive-axle-models/',
        DriveAxleModelList.as_view(),
        name='drive_axle_model_list',
    ),
    path(
        'references/drive-axle-models/create/',
        DriveAxleModelCreate.as_view(),
        name='drive_axle_model_create',
    ),
    path(
        'references/drive-axle-models/<int:pk>/update/',
        DriveAxleModelUpdate.as_view(),
        name='drive_axle_model_update',
    ),

    path(
        'references/steering-axle-models/',
        SteeringAxleModelList.as_view(),
        name='steering_axle_model_list',
    ),
    path(
        'references/steering-axle-models/create/',
        SteeringAxleModelCreate.as_view(),
        name='steering_axle_model_create',
    ),
    path(
        'references/steering-axle-models/<int:pk>/update/',
        SteeringAxleModelUpdate.as_view(),
        name='steering_axle_model_update',
    ),
]
