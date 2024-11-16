from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError
from rest_framework.test import APIRequestFactory

from user_config.serializers import AuthTokenSerializer

User = get_user_model()


class AuthTokenSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword123"
        )
        self.factory = APIRequestFactory()

    def test_authenticate_user(self):
        data = {"email": "testuser@example.com", "password": "testpassword123"}
        request = self.factory.post("/auth/token/")
        serializer = AuthTokenSerializer(data=data, context={"request": request})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["user"], self.user)

    def test_authenticate_user_invalid_credentials(self):
        data = {"email": "testuser@example.com", "password": "wrongpassword"}
        request = self.factory.post("/auth/token/")
        serializer = AuthTokenSerializer(data=data, context={"request": request})
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_authenticate_user_missing_fields(self):
        data = {"email": "testuser@example.com"}
        request = self.factory.post("/auth/token/")
        serializer = AuthTokenSerializer(data=data, context={"request": request})
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
