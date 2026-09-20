from django.urls import path

from .views import (
    MaintenanceCreate,
    MaintenanceDetail,
    MaintenanceList,
    MaintenanceOrganizationCreate,
    MaintenanceOrganizationList,
    MaintenanceOrganizationUpdate,
    MaintenanceTypeCreate,
    MaintenanceTypeList,
    MaintenanceTypeUpdate,
    MaintenanceUpdate,
)


app_name = 'service'

urlpatterns = [
    path('', MaintenanceList.as_view(), name='list'),
    path('create/', MaintenanceCreate.as_view(), name='create'),
    path('<int:pk>/', MaintenanceDetail.as_view(), name='detail'),
    path('<int:pk>/update/', MaintenanceUpdate.as_view(), name='update'),

    path(
        'references/maintenance-types/',
        MaintenanceTypeList.as_view(),
        name='maintenance_type_list',
    ),
    path(
        'references/maintenance-types/create/',
        MaintenanceTypeCreate.as_view(),
        name='maintenance_type_create',
    ),
    path(
        'references/maintenance-types/<int:pk>/update/',
        MaintenanceTypeUpdate.as_view(),
        name='maintenance_type_update',
    ),

    path(
        'references/maintenance-organizations/',
        MaintenanceOrganizationList.as_view(),
        name='maintenance_organization_list',
    ),
    path(
        'references/maintenance-organizations/create/',
        MaintenanceOrganizationCreate.as_view(),
        name='maintenance_organization_create',
    ),
    path(
        'references/maintenance-organizations/<int:pk>/update/',
        MaintenanceOrganizationUpdate.as_view(),
        name='maintenance_organization_update',
    ),
]
