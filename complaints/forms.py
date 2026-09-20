from django import forms
from django.contrib.auth.models import User

from core.access import get_complaint_write_machines
from core.user_choices import UserChoiceField

from .models import (
    Complaint,
    FailureNode,
    RecoveryMethod,
)


class ComplaintForm(forms.ModelForm):
    service_company = UserChoiceField(
        queryset=(
            User.objects
            .filter(groups__name='service')
            .distinct()
        ),
        label='Сервисная компания',
    )

    class Meta:
        model = Complaint
        fields = [
            'failure_date',
            'operating_time',
            'failure_node',
            'failure_description',
            'recovery_method',
            'spare_parts',
            'recovery_date',
            'machine',
            'service_company',
        ]

        widgets = {
            'failure_date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d',
            ),
            'recovery_date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d',
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user is None:
            return

        self.fields['machine'].queryset = get_complaint_write_machines(user)

        groups = set(user.groups.values_list('name', flat=True))

        if user.is_superuser or 'manager' in groups:
            self.fields['service_company'].queryset = (
                User.objects
                .filter(groups__name='service')
                .distinct()
            )
        # Service users can only work with their own service company.
        elif 'service' in groups:
            if self.instance and self.instance.pk:
                service_company = self.instance.service_company
            else:
                service_company = user

            self.fields['service_company'].queryset = User.objects.filter(
                pk=service_company.pk
            )
            self.fields['service_company'].initial = service_company
            self.fields['service_company'].disabled = True


class FailureNodeForm(forms.ModelForm):
    class Meta:
        model = FailureNode
        fields = [
            'name',
            'description',
        ]


class RecoveryMethodForm(forms.ModelForm):
    class Meta:
        model = RecoveryMethod
        fields = [
            'name',
            'description',
        ]
