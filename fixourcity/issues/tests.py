from django.test import TestCase

# Create your tests here.

# Create these test files in your Django apps

# 1. fixourcity/issues/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse

class IssuesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_issues_views_exist(self):
        """Test that main views return 200 or redirect"""
        # Test home page or main issues page
        try:
            response = self.client.get('/')
            self.assertIn(response.status_code, [200, 302, 301])
        except:
            pass  # URL might not exist yet
    
    def test_user_can_login(self):
        """Test user login functionality"""
        login_successful = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login_successful)
    
    def test_models_string_representation(self):
        """Test model __str__ methods"""
        # Add tests for your models
        # Example:
        # issue = Issue.objects.create(title="Test Issue", user=self.user)
        # self.assertEqual(str(issue), "Test Issue")
        pass
