from django import forms
from django.contrib.auth.models import User

from core.user_choices import UserChoiceField

from .models import (
    DriveAxleModel,
    EngineModel,
    Machine,
    SteeringAxleModel,
    TechniqueModel,
    TransmissionModel,
)


class MachineForm(forms.ModelForm):
    client = UserChoiceField(
        queryset=(
            User.objects.filter(groups__name='client')
            .distinct()
            .order_by('username')
        ),
        label='Клиент',
    )

    service_company = UserChoiceField(
        queryset=(
            User.objects.filter(groups__name='service')
            .distinct()
            .order_by('username')
        ),
        label='Сервисная компания',
    )

    class Meta:
        model = Machine
        fields = [
            'factory_number',
            'technique_model',
            'engine_model',
            'engine_factory_number',
            'transmission_model',
            'transmission_factory_number',
            'drive_axle_model',
            'drive_axle_factory_number',
            'steering_axle_model',
            'steering_axle_factory_number',
            'supply_contract',
            'shipment_date',
            'consignee',
            'delivery_address',
            'equipment',
            'client',
            'service_company',
        ]
        widgets = {
            'shipment_date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d',
            ),
        }


class TechniqueModelForm(forms.ModelForm):
    class Meta:
        model = TechniqueModel
        fields = [
            'name',
            'description',
        ]


class EngineModelForm(forms.ModelForm):
    class Meta:
        model = EngineModel
        fields = [
            'name',
            'description',
        ]


class TransmissionModelForm(forms.ModelForm):
    class Meta:
        model = TransmissionModel
        fields = [
            'name',
            'description',
        ]


class DriveAxleModelForm(forms.ModelForm):
    class Meta:
        model = DriveAxleModel
        fields = [
            'name',
            'description',
        ]


class SteeringAxleModelForm(forms.ModelForm):
    class Meta:
        model = SteeringAxleModel
        fields = [
            'name',
            'description',
        ]
