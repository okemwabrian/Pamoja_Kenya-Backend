#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from accounts.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

def debug_authentication():
    print("=== AUTHENTICATION DEBUG ===")
    
    # Get admin user
    admin_user = User.objects.get(username='admin')
    print(f"Admin user: {admin_user.username}")
    print(f"Password hash: {admin_user.password[:50]}...")
    
    # Test password directly
    password_check = check_password('admin123', admin_user.password)
    print(f"Direct password check: {password_check}")
    
    # Test with different passwords
    test_passwords = ['admin123', 'Admin123', 'ADMIN123']
    
    for pwd in test_passwords:
        print(f"\nTesting password: '{pwd}'")
        
        # Direct password check
        direct_check = check_password(pwd, admin_user.password)
        print(f"  Direct check: {direct_check}")
        
        # Django authenticate
        auth_user = authenticate(username='admin', password=pwd)
        print(f"  Django auth: {'Success' if auth_user else 'Failed'}")
    
    # Create a fresh admin user
    print("\n=== CREATING FRESH ADMIN ===")
    try:
        # Delete existing admin
        User.objects.filter(username='admin').delete()
        
        # Create new admin
        new_admin = User.objects.create_user(
            username='admin',
            email='admin@pamojakenyamn.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        new_admin.is_staff = True
        new_admin.is_superuser = True
        new_admin.save()
        
        print(f"Created fresh admin: {new_admin.username}")
        
        # Test authentication
        test_auth = authenticate(username='admin', password='admin123')
        print(f"Fresh admin auth test: {'Success' if test_auth else 'Failed'}")
        
        if test_auth:
            print(f"Authenticated as: {test_auth.username}")
            print(f"Is staff: {test_auth.is_staff}")
            print(f"Is superuser: {test_auth.is_superuser}")
        
    except Exception as e:
        print(f"Error creating fresh admin: {e}")

if __name__ == '__main__':
    debug_authentication()