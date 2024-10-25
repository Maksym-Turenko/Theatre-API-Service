from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError

from user_config.serializers import UserSerializer


User = get_user_model()


class UserSerializerTests(TestCase):

    def test_create_user(self):
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123",
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, data["username"])
        self.assertEqual(user.email, data["email"])
        self.assertTrue(user.check_password(data["password"]))

    def test_update_user(self):
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="initialpassword",
        )
        data = {
            "username": "updateduser",
            "email": "updateduser@example.com",
            "password": "updatedpassword123",
        }
        serializer = UserSerializer(instance=user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        self.assertEqual(updated_user.username, data["username"])
        self.assertEqual(updated_user.email, data["email"])
        self.assertTrue(updated_user.check_password(data["password"]))

    def test_create_user_missing_password(self):
        data = {"username": "testuser", "email": "testuser@example.com"}
        serializer = UserSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
