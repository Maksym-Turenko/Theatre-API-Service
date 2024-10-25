from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group, ContentType


User = get_user_model()


class UserModelTests(TestCase):
    def test_create_user_with_email(self):
        email = "testuser@example.com"
        password = "testpassword"
        user = User.objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser_with_email(self):
        email = "superuser@example.com"
        password = "superpassword"
        user = User.objects.create_superuser(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user_no_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="testpassword")

    def test_user_permissions(self):
        user = User.objects.create_user(
            email="userwithpermissions@example.com", password="password"
        )
        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.create(
            codename="test_permission",
            name="Test Permission",
            content_type=content_type,
        )
        user.user_permissions.add(permission)
        self.assertTrue(
            user.user_permissions.filter(codename="test_permission").exists()
        )

    def test_user_groups(self):
        user = User.objects.create_user(
            email="userwithgroups@example.com", password="password"
        )
        group = Group.objects.create(name="Test Group")
        user.groups.add(group)
        self.assertTrue(user.groups.filter(name="Test Group").exists())
