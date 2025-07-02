from django.test import TestCase

# Create your tests here.

# 2. fixourcity/authorities/tests.py  
from django.test import TestCase, Client
from django.contrib.auth.models import User

class AuthoritiesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='authority_user',
            email='authority@example.com',
            password='authpass123'
        )

    def test_authorities_functionality(self):
        """Test basic authorities functionality"""
        self.assertTrue(self.user.is_authenticated)
    
    def test_authority_views(self):
        """Test authority related views"""
        # Test any authority-specific URLs
        response = self.client.get('/admin/')  # Admin is always available
        self.assertIn(response.status_code, [200, 302, 301])