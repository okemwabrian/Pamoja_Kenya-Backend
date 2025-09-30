#!/usr/bin/env python
import os
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from accounts.models import User
from django.contrib.auth import authenticate

# Test user creation and authentication
user, created = User.objects.get_or_create(
    email='simpletest@example.com',
    defaults={
        'username': 'simpletest',
        'first_name': 'Simple',
        'last_name': 'Test'
    }
)
user.set_password('simplepass123')
user.save()

print(f"User created: {created}")
print(f"User email: {user.email}")
print(f"User active: {user.is_active}")

# Test authentication
auth_user = authenticate(username='simpletest@example.com', password='simplepass123')
print(f"Authentication result: {auth_user}")

# Test API login
login_data = {
    'identifier': 'simpletest@example.com',
    'password': 'simplepass123'
}

try:
    response = requests.post(
        'http://localhost:8000/api/auth/login/',
        json=login_data,
        headers={'Content-Type': 'application/json'}
    )
    print(f"API Response Status: {response.status_code}")
    print(f"API Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        token = data['tokens']['access']
        print(f"Token received: {token[:50]}...")
        
        # Test application creation
        app_data = {
            "application_type": "single",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "phone": "1234567890",
            "address": "123 Main St",
            "city": "Minneapolis",
            "state": "MN",
            "zip_code": "55401",
            "date_of_birth": "1990-01-01",
            "gender": "male",
            "marital_status": "single",
            "occupation": "Engineer",
            "employer": "Tech Corp",
            "annual_income": 50000,
            "emergency_contact_name": "Jane Doe",
            "emergency_contact_phone": "0987654321",
            "emergency_contact_relationship": "Sister"
        }
        
        app_response = requests.post(
            'http://localhost:8000/api/applications/submit/',
            json=app_data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
        )
        print(f"Application Response Status: {app_response.status_code}")
        print(f"Application Response: {app_response.text}")
        
except Exception as e:
    print(f"Error: {e}")