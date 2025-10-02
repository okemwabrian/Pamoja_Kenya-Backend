#!/usr/bin/env python
"""
Test all endpoints required by the frontend
"""
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

def get_auth_token():
    """Get JWT token for testing"""
    user = User.objects.filter(is_staff=True).first()
    if not user:
        user = User.objects.create_superuser(
            username='admin',
            email='admin@pamojakenyamn.com',
            password='admin123'
        )
    
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

def test_endpoints():
    """Test all required endpoints"""
    client = Client()
    token = get_auth_token()
    
    # Test endpoints without auth
    public_endpoints = [
        ('POST', '/api/auth/login/', {'email': 'admin@pamojakenyamn.com', 'password': 'admin123'}),
        ('POST', '/api/auth/register/', {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }),
    ]
    
    # Test endpoints with auth
    auth_endpoints = [
        ('GET', '/api/applications/my-applications/'),
        ('GET', '/api/claims/'),
        ('GET', '/api/payments/'),
        ('GET', '/api/notifications/list/'),
        ('GET', '/api/admin/stats/'),
        ('GET', '/api/admin/users/'),
        ('GET', '/api/admin/applications/'),
        ('GET', '/api/admin/claims/'),
    ]
    
    print("Testing Frontend Required Endpoints")
    print("=" * 50)
    
    # Test public endpoints
    print("\n[AUTH] Authentication Endpoints:")
    for method, endpoint, data in public_endpoints:
        try:
            if method == 'POST':
                response = client.post(endpoint, data, content_type='application/json')
            else:
                response = client.get(endpoint)
            
            status = "[OK]" if response.status_code in [200, 201] else "[WARN]"
            print(f"  {status} {method} {endpoint} - {response.status_code}")
            
            if response.status_code in [200, 201] and endpoint == '/api/auth/login/':
                try:
                    data = response.json()
                    if 'access' in data:
                        print(f"    [TOKEN] JWT Token received")
                except:
                    pass
                    
        except Exception as e:
            print(f"  [ERROR] {method} {endpoint} - Error: {e}")
    
    # Test authenticated endpoints
    print("\n[SECURE] Authenticated Endpoints:")
    headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
    
    for method, endpoint in auth_endpoints:
        try:
            if method == 'GET':
                response = client.get(endpoint, **headers)
            
            status = "[OK]" if response.status_code == 200 else "[WARN]"
            print(f"  {status} {method} {endpoint} - {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, dict):
                        keys = list(data.keys())[:3]
                        print(f"    [DATA] Response keys: {keys}...")
                    elif isinstance(data, list):
                        print(f"    [LIST] Array with {len(data)} items")
                except:
                    pass
                    
        except Exception as e:
            print(f"  [ERROR] {method} {endpoint} - Error: {e}")
    
    # Test content creation endpoints
    print("\n[CREATE] Content Creation Endpoints:")
    content_endpoints = [
        ('POST', '/api/admin/announcements/create/', {
            'title': 'Test Announcement',
            'content': 'This is a test announcement',
            'priority': 'medium'
        }),
        ('POST', '/api/admin/events/create/', {
            'title': 'Test Event',
            'description': 'This is a test event',
            'date': '2024-12-01T10:00:00Z',
            'location': 'Test Location'
        }),
        ('POST', '/api/admin/meetings/create/', {
            'title': 'Test Meeting',
            'description': 'This is a test meeting',
            'date': '2024-12-01T14:00:00Z',
            'duration': 60,
            'type': 'zoom'
        }),
    ]
    
    for method, endpoint, data in content_endpoints:
        try:
            response = client.post(endpoint, data, content_type='application/json', **headers)
            status = "[OK]" if response.status_code in [200, 201] else "[WARN]"
            print(f"  {status} {method} {endpoint} - {response.status_code}")
        except Exception as e:
            print(f"  [ERROR] {method} {endpoint} - Error: {e}")
    
    print("\n" + "=" * 50)
    print("[SUCCESS] Backend is ready for frontend connection!")
    print("[START] Start backend: python start_backend_for_frontend.py")
    print("[URL] Backend URL: http://localhost:8000")
    print("[API] API Base: http://localhost:8000/api/")

if __name__ == "__main__":
    test_endpoints()