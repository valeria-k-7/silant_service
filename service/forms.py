from django import forms
from django.contrib.auth.models import User

from core.access import get_accessible_machines
from core.user_choices import UserChoiceField

from .models import (
    Maintenance,
    MaintenanceOrganization,
    MaintenanceType,
)


class MaintenanceForm(forms.ModelForm):
    service_company = UserChoiceField(
        queryset=(
            User.objects
            .filter(groups__name='service')
            .distinct()
        ),
        label='Сервисная компания',
    )

    class Meta:
        model = Maintenance
        fields = [
            'maintenance_type',
            'maintenance_date',
            'operating_time',
            'work_order_number',
            'work_order_date',
            'organization',
            'machine',
            'service_company',
        ]

        widgets = {
            'maintenance_date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d',
            ),
            'work_order_date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d',
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields['machine'].queryset = get_accessible_machines(user)


class MaintenanceTypeForm(forms.ModelForm):
    class Meta:
        model = MaintenanceType
        fields = [
            'name',
            'description',
        ]


class MaintenanceOrganizationForm(forms.ModelForm):
    class Meta:
        model = MaintenanceOrganization
        fields = [
            'name',
            'description',
        ]
