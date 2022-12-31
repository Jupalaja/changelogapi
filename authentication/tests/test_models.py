from rest_framework.test import APITestCase
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
import jwt
from authentication.models import User


class TestsModel(APITestCase):

    def test_creates_user(self):
        user = User.objects.create_user('juan', 'juan@gmail.com', 'password')
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'juan')
        self.assertEqual(user.email, 'juan@gmail.com')
        self.assertFalse(user.is_staff)

    def test_creates_superuser(self):
        user = User.objects.create_superuser('juan', 'juan@gmail.com', 'password')
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'juan')
        self.assertTrue(user.is_staff)

    def test_raises_error_with_message_when_no_username_is_provided(self):
        with self.assertRaisesMessage(ValueError, 'The given username must be set'):
            User.objects.create_user('', 'juan@gmail.com', 'password')

    def test_raises_error_with_message_when_no_email_is_provided(self):
        with self.assertRaisesMessage(ValueError, 'The given email must be set'):
            User.objects.create_user('juan', '', 'password')

    def test_create_super_user_with_staff_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_staff=True.'):
            User.objects.create_superuser('juan', 'juan@gmail.com', 'password', is_staff=False)

    def test_create_super_user_with_superuser_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_superuser=True.'):
            User.objects.create_superuser('juan', 'juan@gmail.com', 'password', is_superuser=False)

    def test_response_token(self):
        user = User.objects.create_superuser('juan', 'juan@gmail.com', 'password')
        self.assertEqual(user.token,
                         jwt.encode(
                             {'username': 'juan', 'email': 'juan@gmail.com',
                              'exp': datetime.utcnow() + timedelta(hours=24)},
                             settings.SECRET_KEY, algorithm="HS256")
                         )
