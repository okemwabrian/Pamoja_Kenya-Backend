#!/usr/bin/env python
"""
Test script to verify all content management endpoints are working
"""
import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model
from notifications.models import Announcement, Event, Meeting

User = get_user_model()

def test_content_management_endpoints():
    """Test all content management endpoints"""
    client = Client()
    
    # Create admin user for testing
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
    
    print("🧪 Testing Content Management Endpoints")
    print("=" * 50)
    
    # Test Admin Endpoints
    admin_endpoints = [
        # Announcements
        ('/api/admin/announcements/', 'GET', 'List announcements'),
        ('/api/admin/announcements/create/', 'POST', 'Create announcement'),
        
        # Events  
        ('/api/admin/events/', 'GET', 'List events'),
        ('/api/admin/events/create/', 'POST', 'Create event'),
        
        # Meetings
        ('/api/admin/meetings/', 'GET', 'List meetings'),
        ('/api/admin/meetings/create/', 'POST', 'Create meeting'),
    ]
    
    # Test Public Endpoints
    public_endpoints = [
        ('/api/notifications/announcements/', 'GET', 'Public announcements'),
        ('/api/notifications/events/', 'GET', 'Public events'),
    ]
    
    print("📋 Admin Endpoints:")
    for endpoint, method, description in admin_endpoints:
        try:
            if method == 'GET':
                response = client.get(endpoint)
            elif method == 'POST':
                # Test data for POST requests
                if 'announcement' in endpoint:
                    data = {
                        'title': 'Test Announcement',
                        'content': 'Test content',
                        'priority': 'medium',
                        'is_pinned': False
                    }
                elif 'event' in endpoint:
                    data = {
                        'title': 'Test Event',
                        'description': 'Test description',
                        'date': '2024-12-31T18:00:00Z',
                        'location': 'Test Location',
                        'is_featured': False,
                        'registration_required': True
                    }
                elif 'meeting' in endpoint:
                    data = {
                        'title': 'Test Meeting',
                        'description': 'Test description',
                        'date': '2024-12-31T18:00:00Z',
                        'duration': 60,
                        'type': 'zoom',
                        'max_participants': 100,
                        'meeting_link': 'https://zoom.us/test',
                        'require_registration': True
                    }
                response = client.post(endpoint, data, content_type='application/json')
            
            status_icon = "✅" if response.status_code < 400 else "❌"
            print(f"  {status_icon} {method} {endpoint} - {description} ({response.status_code})")
            
        except Exception as e:
            print(f"  ❌ {method} {endpoint} - {description} (ERROR: {str(e)})")
    
    print("\n🌐 Public Endpoints:")
    client.logout()  # Test as anonymous user
    
    for endpoint, method, description in public_endpoints:
        try:
            response = client.get(endpoint)
            status_icon = "✅" if response.status_code < 400 else "❌"
            print(f"  {status_icon} {method} {endpoint} - {description} ({response.status_code})")
        except Exception as e:
            print(f"  ❌ {method} {endpoint} - {description} (ERROR: {str(e)})")
    
    print("\n📊 Database Content:")
    print(f"  📢 Announcements: {Announcement.objects.count()}")
    print(f"  📅 Events: {Event.objects.count()}")
    print(f"  🤝 Meetings: {Meeting.objects.count()}")
    
    print("\n✨ Content Management Test Complete!")

if __name__ == '__main__':
    test_content_management_endpoints()