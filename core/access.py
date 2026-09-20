from django.db.models import Q

from complaints.models import Complaint
from machines.models import Machine
from service.models import Maintenance


def get_accessible_machines(user):
    if not user.is_authenticated:
        return Machine.objects.none()

    if user.is_superuser:
        return Machine.objects.all()

    groups = set(user.groups.values_list('name', flat=True))

    if 'manager' in groups:
        return Machine.objects.all()

    # Both roles can access machines from client and service scopes.
    if 'client' in groups and 'service' in groups:
        return Machine.objects.filter(
            Q(client=user) | Q(service_company=user)
        ).distinct()

    if 'client' in groups:
        return Machine.objects.filter(client=user)

    if 'service' in groups:
        return Machine.objects.filter(service_company=user)

    return Machine.objects.none()


def get_accessible_maintenance(user):
    return Maintenance.objects.filter(
        machine__in=get_accessible_machines(user)
    )


def get_accessible_complaints(user):
    return Complaint.objects.filter(
        machine__in=get_accessible_machines(user)
    )


def get_complaint_write_machines(user):
    if not user.is_authenticated:
        return Machine.objects.none()

    if user.is_superuser:
        return Machine.objects.all()

    groups = set(user.groups.values_list('name', flat=True))

    if 'manager' in groups:
        return Machine.objects.all()

    # Complaint editing is limited to the user's service scope.
    if 'service' in groups:
        return Machine.objects.filter(service_company=user)

    return Machine.objects.none()


def get_editable_complaints(user):
    return Complaint.objects.filter(
        machine__in=get_complaint_write_machines(user)
    )
