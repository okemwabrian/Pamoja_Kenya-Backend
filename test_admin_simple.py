#!/usr/bin/env python
"""
Simple test for admin endpoints
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

def test_admin_endpoints():
    # Get admin user
    admin_user = User.objects.get(username='admin')
    print(f"Admin user: {admin_user.username} - Staff: {admin_user.is_staff} - Role: {admin_user.role}")
    
    # Create JWT token
    refresh = RefreshToken.for_user(admin_user)
    access_token = str(refresh.access_token)
    
    # Create API client
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    
    # Test admin stats endpoint
    response = client.get('/api/admin/stats/')
    print(f"Admin stats: {response.status_code}")
    if response.status_code == 200:
        print("SUCCESS: Admin stats endpoint working")
        print(f"Response: {response.json()}")
    else:
        print(f"FAILED: {response.content}")
    
    # Test users list
    response = client.get('/api/admin/users/')
    print(f"Users list: {response.status_code}")
    if response.status_code == 200:
        print("SUCCESS: Users list endpoint working")
        data = response.json()
        print(f"Found {len(data)} users")
    else:
        print(f"FAILED: {response.content}")

if __name__ == "__main__":
    test_admin_endpoints()