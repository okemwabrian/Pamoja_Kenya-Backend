#!/usr/bin/env python
"""
Simple Backend Verification Test
"""
import os
import sys
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def test_backend():
    """Test critical backend functionality"""
    client = Client()
    
    print("BACKEND VERIFICATION RESULTS")
    print("=" * 40)
    
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
    
    # Test 1: JWT Authentication
    login_data = {'username': 'admin', 'password': 'admin123'}
    response = client.post('/api/auth/login/', 
                          data=json.dumps(login_data), 
                          content_type='application/json')
    
    auth_working = response.status_code == 200
    print(f"1. JWT Authentication: {'PASS' if auth_working else 'FAIL'} ({response.status_code})")
    
    # Test 2: Home Page Content
    response = client.get('/api/notifications/announcements/?limit=2')
    announcements_working = response.status_code == 200
    print(f"2. Announcements (limit=2): {'PASS' if announcements_working else 'FAIL'} ({response.status_code})")
    
    response = client.get('/api/notifications/events/?limit=2')
    events_working = response.status_code == 200
    print(f"3. Events (limit=2): {'PASS' if events_working else 'FAIL'} ({response.status_code})")
    
    # Test 3: Admin Content Creation
    client.force_login(admin_user)
    
    announcement_data = {
        'title': 'Test Announcement',
        'content': 'Test content',
        'priority': 'medium'
    }
    response = client.post('/api/admin/announcements/create/', 
                          data=json.dumps(announcement_data), 
                          content_type='application/json')
    admin_create_working = response.status_code == 201
    print(f"4. Admin Create Content: {'PASS' if admin_create_working else 'FAIL'} ({response.status_code})")
    
    # Test 4: Applications
    app_data = {
        'application_type': 'single',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'phone': '+1234567890',
        'address': '123 Main St',
        'city': 'Test City',
        'state': 'CA',
        'zip_code': '12345',
        'amount': 200.00,
        'constitution_agreed': True
    }
    response = client.post('/api/applications/submit/', 
                          data=json.dumps(app_data), 
                          content_type='application/json')
    app_working = response.status_code == 201
    print(f"5. Single Application ($200): {'PASS' if app_working else 'FAIL'} ({response.status_code})")
    
    # Test 5: PayPal Payments
    payment_data = {
        'payer_name': 'John Doe',
        'payer_email': 'john@example.com',
        'paypal_order_id': 'PAYPAL123',
        'amount': 200.00,
        'currency': 'USD'
    }
    response = client.post('/api/payments/paypal/', 
                          data=json.dumps(payment_data), 
                          content_type='application/json')
    payment_working = response.status_code == 201
    print(f"6. PayPal Payment: {'PASS' if payment_working else 'FAIL'} ({response.status_code})")
    
    print("\n" + "=" * 40)
    
    all_tests = [auth_working, announcements_working, events_working, 
                admin_create_working, app_working, payment_working]
    
    if all(all_tests):
        print("RESULT: ALL CRITICAL TESTS PASSED!")
        print("Backend is ready for frontend integration.")
    else:
        print(f"RESULT: {sum(all_tests)}/6 tests passed")
        print("Some functionality needs attention.")
    
    print("\nCURL Test Commands:")
    print('curl -X POST http://localhost:8000/api/auth/login/ -H "Content-Type: application/json" -d \'{"username":"admin","password":"admin123"}\'')
    print('curl -X GET "http://localhost:8000/api/notifications/announcements/?limit=2"')

if __name__ == '__main__':
    test_backend()