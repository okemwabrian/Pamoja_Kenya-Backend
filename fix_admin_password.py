#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from accounts.models import User
from django.contrib.auth import authenticate

def fix_admin_password():
    print("Fixing admin password...")
    
    try:
        admin_user = User.objects.get(username='admin')
        print(f"Found admin user: {admin_user.username}")
        
        # Set password
        admin_user.set_password('admin123')
        admin_user.save()
        print("Password set to: admin123")
        
        # Test authentication
        test_user = authenticate(username='admin', password='admin123')
        if test_user:
            print("[OK] Authentication test successful!")
            print(f"User: {test_user.username}")
            print(f"Email: {test_user.email}")
            print(f"Staff: {test_user.is_staff}")
            print(f"Superuser: {test_user.is_superuser}")
            return True
        else:
            print("[ERROR] Authentication test failed!")
            return False
            
    except User.DoesNotExist:
        print("Admin user not found! Creating new admin user...")
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@pamojakenyamn.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        print(f"Created admin user: {admin_user.username}")
        return True

if __name__ == '__main__':
    fix_admin_password()