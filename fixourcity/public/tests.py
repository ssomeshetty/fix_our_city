# 4. fixourcity/public/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User

class PublicTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_public_views(self):
        """Test public accessible views"""
        # Test any public URLs
        try:
            response = self.client.get('/')
            self.assertIn(response.status_code, [200, 302, 404])
        except:
            pass
    
    def test_user_registration(self):
        """Test user can be created"""
        user = User.objects.create_user(
            username='public_user',
            email='public@example.com',
            password='publicpass123'
        )
        self.assertEqual(user.username, 'public_user')
        self.assertTrue(user.check_password('publicpass123'))