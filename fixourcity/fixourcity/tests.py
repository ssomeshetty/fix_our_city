
# 5. fixourcity/fixourcity/tests.py (Main project tests)
from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings

class MainProjectTestCase(TestCase):
    def test_settings_configuration(self):
        """Test basic settings are configured"""
        self.assertIsNotNone(settings.SECRET_KEY)
        self.assertIsInstance(settings.INSTALLED_APPS, list)
        self.assertTrue(len(settings.INSTALLED_APPS) > 0)
    
    def test_database_connection(self):
        """Test database connection works"""
        user = User.objects.create_user(
            username='db_test_user',
            email='dbtest@example.com',
            password='dbtest123'
        )
        self.assertEqual(User.objects.filter(username='db_test_user').count(), 1)
        user.delete()
        self.assertEqual(User.objects.filter(username='db_test_user').count(), 0)
    
    def test_admin_user_creation(self):
        """Test admin user can be created"""
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)
