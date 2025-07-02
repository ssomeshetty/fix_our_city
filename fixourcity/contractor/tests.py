from django.test import TestCase

# Create your tests here.
# 3. fixourcity/contractor/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User

class ContractorTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='contractor_user',
            email='contractor@example.com',
            password='contractorpass123'
        )

    def test_contractor_functionality(self):
        """Test basic contractor functionality"""
        self.assertTrue(self.user.is_authenticated)
        self.assertEqual(self.user.username, 'contractor_user')
    
    def test_contractor_models(self):
        """Test contractor models if they exist"""
        # Add specific contractor model tests here
        pass
