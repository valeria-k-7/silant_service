from django.core.exceptions import PermissionDenied


def account_management_disabled(request):
    raise PermissionDenied(
        'Самостоятельное управление учётной записью запрещено.'
    )
