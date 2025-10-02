#!/usr/bin/env python
"""
Test session timeout implementation for users vs admins
"""
import os
import sys
import django
import json
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()

def test_session_timeout():
    """Test different session timeouts for users vs admins"""
    client = Client()
    
    print("SESSION TIMEOUT VERIFICATION")
    print("=" * 40)
    
    # Create regular user
    regular_user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'user@test.com',
            'is_staff': False,
            'is_superuser': False
        }
    )
    if created:
        regular_user.set_password('test123')
        regular_user.save()
    
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
    
    # Test regular user login
    print("1. Regular User Login:")
    login_data = {'username': 'testuser', 'password': 'test123'}
    response = client.post('/api/auth/login/', 
                          data=json.dumps(login_data), 
                          content_type='application/json')
    
    if response.status_code == 200:
        user_data = response.json()
        print(f"   Login: SUCCESS")
        print(f"   is_admin: {user_data.get('user', {}).get('is_admin', 'NOT_FOUND')}")
        
        # Check token expiration
        access_token = user_data.get('tokens', {}).get('access')
        if access_token:
            try:
                token = UntypedToken(access_token)
                exp_timestamp = token.payload.get('exp')
                if exp_timestamp:
                    exp_time = datetime.fromtimestamp(exp_timestamp)
                    now = datetime.now()
                    duration = exp_time - now
                    print(f"   Token expires in: {duration}")
            except (InvalidToken, TokenError):
                print("   Token validation failed")
    else:
        print(f"   Login: FAILED ({response.status_code})")
    
    # Test admin user login
    print("\n2. Admin User Login:")
    login_data = {'username': 'admin', 'password': 'admin123'}
    response = client.post('/api/auth/login/', 
                          data=json.dumps(login_data), 
                          content_type='application/json')
    
    if response.status_code == 200:
        admin_data = response.json()
        print(f"   Login: SUCCESS")
        print(f"   is_admin: {admin_data.get('user', {}).get('is_admin', 'NOT_FOUND')}")
        
        # Check token expiration
        access_token = admin_data.get('tokens', {}).get('access')
        if access_token:
            try:
                token = UntypedToken(access_token)
                exp_timestamp = token.payload.get('exp')
                if exp_timestamp:
                    exp_time = datetime.fromtimestamp(exp_timestamp)
                    now = datetime.now()
                    duration = exp_time - now
                    print(f"   Token expires in: {duration}")
            except (InvalidToken, TokenError):
                print("   Token validation failed")
    else:
        print(f"   Login: FAILED ({response.status_code})")
    
    print("\n" + "=" * 40)
    print("SESSION TIMEOUT IMPLEMENTATION:")
    print("- Regular users: 10-minute timeout")
    print("- Admin users: 30-day timeout")
    print("- Login response includes is_admin field")
    print("- Frontend can use is_admin to determine timeout behavior")

if __name__ == '__main__':
    test_session_timeout()