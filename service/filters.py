from django.contrib.auth.models import User
from django_filters import CharFilter, FilterSet, ModelChoiceFilter

from core.user_choices import UserChoiceFilter

from .models import Maintenance, MaintenanceType


class MaintenanceFilter(FilterSet):
    maintenance_type = ModelChoiceFilter(
        queryset=MaintenanceType.objects.all(),
        label='Вид ТО',
    )

    machine_factory_number = CharFilter(
        field_name='machine__factory_number',
        lookup_expr='icontains',
        label='Зав. № машины',
    )

    service_company = UserChoiceFilter(
        field_name='service_company',
        queryset=User.objects.filter(groups__name='service').distinct(),
        label='Сервисная компания',
    )

    class Meta:
        model = Maintenance
        fields = []
