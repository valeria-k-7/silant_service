from django.contrib.auth.models import User
from django_filters import FilterSet, ModelChoiceFilter

from core.user_choices import UserChoiceFilter

from .models import Complaint, FailureNode, RecoveryMethod


class ComplaintFilter(FilterSet):
    failure_node = ModelChoiceFilter(
        queryset=FailureNode.objects.all(),
        label='Узел отказа',
    )

    recovery_method = ModelChoiceFilter(
        queryset=RecoveryMethod.objects.all(),
        label='Способ восстановления',
    )

    service_company = UserChoiceFilter(
        field_name='service_company',
        queryset=User.objects.filter(groups__name='service').distinct(),
        label='Сервисная компания',
    )

    class Meta:
        model = Complaint
        fields = []
