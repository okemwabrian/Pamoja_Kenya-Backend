#!/usr/bin/env python
"""
Simple test to verify content management endpoints
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def test_endpoints():
    """Test content management endpoints"""
    client = Client()
    
    # Create admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@test.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
    
    # Login as admin
    client.force_login(admin_user)
    
    print("Testing Content Management Endpoints")
    print("=" * 40)
    
    # Test endpoints
    endpoints = [
        ('/api/admin/announcements/', 'GET'),
        ('/api/admin/events/', 'GET'),
        ('/api/admin/meetings/', 'GET'),
        ('/api/notifications/announcements/', 'GET'),
        ('/api/notifications/events/', 'GET'),
    ]
    
    for endpoint, method in endpoints:
        try:
            response = client.get(endpoint)
            status = "OK" if response.status_code < 400 else "FAIL"
            print(f"{method} {endpoint} - {status} ({response.status_code})")
        except Exception as e:
            print(f"{method} {endpoint} - ERROR: {str(e)}")
    
    print("\nTest Complete!")

if __name__ == '__main__':
    test_endpoints()