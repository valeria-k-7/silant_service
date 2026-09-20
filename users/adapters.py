from allauth.account.adapter import DefaultAccountAdapter
from django.core.exceptions import PermissionDenied


class SilantAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False

    def set_password(self, user, password):
        raise PermissionDenied('Самостоятельная смена пароля запрещена.')

    def send_password_reset_mail(self, user, email, context):
        raise PermissionDenied('Самостоятельный сброс пароля запрещён.')
