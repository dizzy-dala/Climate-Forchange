import os
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase


User = get_user_model()


class EnsureSuperuserCommandTests(TestCase):
    def test_creates_superuser_from_environment_variables(self):
        with patch.dict(
            os.environ,
            {
                'DJANGO_SUPERUSER_USERNAME': 'deploy-admin',
                'DJANGO_SUPERUSER_EMAIL': 'admin@example.com',
                'DJANGO_SUPERUSER_PASSWORD': 'SuperSecret123!',
            },
            clear=False,
        ):
            call_command('ensure_superuser')

            user = User.objects.get(username='deploy-admin')
            self.assertTrue(user.is_superuser)
            self.assertTrue(user.is_staff)
            self.assertEqual(user.email, 'admin@example.com')
            self.assertTrue(user.check_password('SuperSecret123!'))

    def test_does_not_create_duplicates_when_user_exists(self):
        User.objects.create_superuser(
            username='existing-admin',
            email='existing@example.com',
            password='ExistingPass123!',
        )

        with patch.dict(
            os.environ,
            {
                'DJANGO_SUPERUSER_USERNAME': 'existing-admin',
                'DJANGO_SUPERUSER_EMAIL': 'another@example.com',
                'DJANGO_SUPERUSER_PASSWORD': 'DifferentPass123!',
            },
            clear=False,
        ):
            call_command('ensure_superuser')

        self.assertEqual(User.objects.filter(username='existing-admin').count(), 1)
