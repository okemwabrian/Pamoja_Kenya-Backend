#!/usr/bin/env python
"""
Test script to verify contact system endpoints
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
from notifications.models import ContactMessage, AdminNotification

User = get_user_model()

def test_contact_system():
    """Test contact system endpoints"""
    client = Client()
    
    print("Testing Contact System Endpoints")
    print("=" * 40)
    
    # Test public contact submission
    contact_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'subject': 'Membership Inquiry',
        'help_type': 'membership',
        'message': 'I would like to know more about membership options.',
        'phone': '+1234567890'
    }
    
    print("1. Testing contact submission...")
    response = client.post('/api/contact/submit/', 
                          data=json.dumps(contact_data), 
                          content_type='application/json')
    
    status = "OK" if response.status_code < 400 else "FAIL"
    print(f"   POST /api/contact/submit/ - {status} ({response.status_code})")
    
    if response.status_code == 201:
        print(f"   Contact created with ID: {response.json().get('id')}")
    
    # Create admin user for admin endpoints
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
    
    print("\n2. Testing admin endpoints...")
    
    # Test admin contact list
    response = client.get('/api/notifications/admin/contacts/')
    status = "OK" if response.status_code < 400 else "FAIL"
    print(f"   GET /api/notifications/admin/contacts/ - {status} ({response.status_code})")
    
    # Test admin notifications list
    response = client.get('/api/notifications/admin/notifications/')
    status = "OK" if response.status_code < 400 else "FAIL"
    print(f"   GET /api/notifications/admin/notifications/ - {status} ({response.status_code})")
    
    # Test contact update if we have contacts
    contacts = ContactMessage.objects.all()
    if contacts.exists():
        contact_id = contacts.first().id
        update_data = {
            'status': 'in_progress',
            'admin_notes': 'Following up with customer'
        }
        response = client.patch(f'/api/notifications/admin/contacts/{contact_id}/',
                               data=json.dumps(update_data),
                               content_type='application/json')
        status = "OK" if response.status_code < 400 else "FAIL"
        print(f"   PATCH /api/notifications/admin/contacts/{contact_id}/ - {status} ({response.status_code})")
    
    print("\n3. Database content:")
    print(f"   Contact Messages: {ContactMessage.objects.count()}")
    print(f"   Admin Notifications: {AdminNotification.objects.count()}")
    
    print("\nContact System Test Complete!")

if __name__ == '__main__':
    test_contact_system()