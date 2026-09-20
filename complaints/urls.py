from django.urls import path

from .views import (
    ComplaintCreate,
    ComplaintDetail,
    ComplaintList,
    ComplaintUpdate,
    FailureNodeCreate,
    FailureNodeList,
    FailureNodeUpdate,
    RecoveryMethodCreate,
    RecoveryMethodList,
    RecoveryMethodUpdate,
)


app_name = 'complaints'

urlpatterns = [
    path('', ComplaintList.as_view(), name='list'),
    path('create/', ComplaintCreate.as_view(), name='create'),
    path('<int:pk>/', ComplaintDetail.as_view(), name='detail'),
    path('<int:pk>/update/', ComplaintUpdate.as_view(), name='update'),

    path(
        'references/failure-nodes/',
        FailureNodeList.as_view(),
        name='failure_node_list',
    ),
    path(
        'references/failure-nodes/create/',
        FailureNodeCreate.as_view(),
        name='failure_node_create',
    ),
    path(
        'references/failure-nodes/<int:pk>/update/',
        FailureNodeUpdate.as_view(),
        name='failure_node_update',
    ),

    path(
        'references/recovery-methods/',
        RecoveryMethodList.as_view(),
        name='recovery_method_list',
    ),
    path(
        'references/recovery-methods/create/',
        RecoveryMethodCreate.as_view(),
        name='recovery_method_create',
    ),
    path(
        'references/recovery-methods/<int:pk>/update/',
        RecoveryMethodUpdate.as_view(),
        name='recovery_method_update',
    ),
]
