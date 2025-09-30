#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from django.contrib.auth import authenticate
from accounts.models import User
from accounts.serializers import UserLoginSerializer

def test_admin_login():
    print("=== ADMIN LOGIN DEBUG ===")
    
    # Check if admin user exists
    try:
        admin_user = User.objects.get(username='admin')
        print(f"[OK] Admin user found: {admin_user.username}")
        print(f"   Email: {admin_user.email}")
        print(f"   Active: {admin_user.is_active}")
        print(f"   Staff: {admin_user.is_staff}")
        print(f"   Superuser: {admin_user.is_superuser}")
    except User.DoesNotExist:
        print("[ERROR] Admin user not found!")
        return False
    
    # Test direct authentication
    print("\n=== DIRECT AUTHENTICATION TEST ===")
    user = authenticate(username='admin', password='admin123')
    if user:
        print(f"[OK] Direct auth successful: {user.username}")
    else:
        print("[ERROR] Direct auth failed!")
        return False
    
    # Test serializer
    print("\n=== SERIALIZER TEST ===")
    test_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    serializer = UserLoginSerializer(data=test_data)
    if serializer.is_valid():
        print("[OK] Serializer validation successful")
        user = serializer.validated_data['user']
        print(f"   Authenticated user: {user.username}")
        return True
    else:
        print("[ERROR] Serializer validation failed!")
        print(f"   Errors: {serializer.errors}")
        return False

if __name__ == '__main__':
    test_admin_login()