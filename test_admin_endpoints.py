#!/usr/bin/env python
"""
Test script to verify all admin endpoints are working correctly
"""
import os
import sys
import django
import requests
import json
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

def get_admin_token():
    """Get JWT token for admin user"""
    try:
        admin_user = User.objects.filter(is_staff=True, is_superuser=True).first()
        if not admin_user:
            print("No admin user found. Creating one...")
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@pamojakenyamn.com',
                password='admin123'
            )
        
        refresh = RefreshToken.for_user(admin_user)
        return str(refresh.access_token)
    except Exception as e:
        print(f"Error getting admin token: {e}")
        return None

def test_endpoint(url, method='GET', data=None, token=None):
    """Test an API endpoint"""
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            headers['Content-Type'] = 'application/json'
            response = requests.post(url, headers=headers, json=data)
        elif method == 'PATCH':
            headers['Content-Type'] = 'application/json'
            response = requests.patch(url, headers=headers, json=data)
        
        print(f"{method} {url}: {response.status_code}")
        if response.status_code < 400:
            print("[SUCCESS]")
            if response.content:
                try:
                    result = response.json()
                    if isinstance(result, dict) and len(result) < 10:
                        print(f"Response: {result}")
                    elif isinstance(result, list) and len(result) > 0:
                        print(f"Response: {len(result)} items")
                except:
                    print("Response: Non-JSON content")
        else:
            print("[FAILED]")
            try:
                error = response.json()
                print(f"Error: {error}")
            except:
                print(f"Error: {response.text}")
        print("-" * 50)
        
    except Exception as e:
        print(f"[EXCEPTION]: {e}")
        print("-" * 50)

def main():
    print("Testing Pamoja Kenya Admin API Endpoints")
    print("=" * 50)
    
    # Get admin token
    token = get_admin_token()
    if not token:
        print("Failed to get admin token. Exiting.")
        return
    
    base_url = "http://localhost:8000/api"
    
    # Test admin endpoints
    endpoints = [
        # Dashboard & Stats
        (f"{base_url}/admin/stats/", "GET"),
        
        # User Management
        (f"{base_url}/admin/users/", "GET"),
        
        # Application Management
        (f"{base_url}/admin/applications/", "GET"),
        
        # Claims Management
        (f"{base_url}/admin/claims/", "GET"),
        
        # Payment Management
        (f"{base_url}/admin/payments/", "GET"),
    ]
    
    for url, method in endpoints:
        test_endpoint(url, method, token=token)
    
    # Test content creation endpoints
    print("Testing Content Creation Endpoints")
    print("=" * 50)
    
    # Test announcement creation
    announcement_data = {
        "title": "Test Announcement",
        "content": "This is a test announcement from the admin API",
        "priority": "medium",
        "is_pinned": False
    }
    test_endpoint(f"{base_url}/admin/announcements/create/", "POST", announcement_data, token)
    
    # Test event creation
    future_date = (datetime.now() + timedelta(days=7)).isoformat()
    event_data = {
        "title": "Test Event",
        "description": "This is a test event from the admin API",
        "date": future_date,
        "location": "Test Location",
        "is_featured": False,
        "registration_required": True
    }
    test_endpoint(f"{base_url}/admin/events/create/", "POST", event_data, token)
    
    # Test meeting creation
    meeting_data = {
        "title": "Test Meeting",
        "description": "This is a test meeting from the admin API",
        "date": future_date,
        "duration": 60,
        "type": "zoom",
        "max_participants": 50,
        "meeting_link": "https://zoom.us/j/123456789",
        "require_registration": True,
        "send_notifications": True
    }
    test_endpoint(f"{base_url}/admin/meetings/create/", "POST", meeting_data, token)
    
    print("Admin API endpoint testing completed!")

if __name__ == "__main__":
    main()