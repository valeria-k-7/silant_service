from allauth.account.adapter import get_adapter
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.urls import reverse

from .adapters import SilantAccountAdapter


class AccountRestrictionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='test_user',
            password='TestPassword123!',
        )

    def test_login_page_is_available(self):
        response = self.client.get(
            reverse('account_login')
        )

        self.assertEqual(response.status_code, 200)

    def test_configured_adapter_closes_signup(self):
        adapter = get_adapter()

        self.assertIsInstance(
            adapter,
            SilantAccountAdapter,
        )
        self.assertFalse(
            adapter.is_open_for_signup(None)
        )

    def test_signup_does_not_create_user(self):
        response = self.client.post(
            reverse('account_signup'),
            {
                'username': 'new_user',
                'password1': 'StrongPassword123!',
                'password2': 'StrongPassword123!',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(
                username='new_user'
            ).exists()
        )

    def test_password_change_page_is_forbidden(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse('account_change_password')
        )

        self.assertEqual(response.status_code, 403)

    def test_email_management_page_is_forbidden(self):
        self.client.force_login(self.user)

        get_response = self.client.get(
            reverse('account_email')
        )
        post_response = self.client.post(
            reverse('account_email'),
            {
                'email': 'new@example.com',
                'action_add': '1',
            },
        )

        self.assertEqual(get_response.status_code, 403)
        self.assertEqual(post_response.status_code, 403)

    def test_password_reset_page_is_forbidden(self):
        response = self.client.get(
            reverse('account_reset_password')
        )

        self.assertEqual(response.status_code, 403)

    def test_adapter_rejects_password_change(self):
        adapter = get_adapter()

        with self.assertRaises(PermissionDenied):
            adapter.set_password(
                self.user,
                'AnotherPassword123!',
            )

    def test_adapter_rejects_password_reset_mail(self):
        adapter = get_adapter()

        with self.assertRaises(PermissionDenied):
            adapter.send_password_reset_mail(
                self.user,
                'test@example.com',
                {},
            )
