#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from django.contrib.auth import authenticate
from accounts.models import User

def test_auth_methods():
    print("=== TESTING AUTHENTICATION METHODS ===")
    
    admin_user = User.objects.get(username='admin')
    print(f"Admin user: {admin_user.username}")
    print(f"Admin email: {admin_user.email}")
    
    # Test 1: Direct email authentication
    print("\n1. Testing email authentication:")
    user1 = authenticate(username=admin_user.email, password='admin123')
    print(f"   Result: {'Success' if user1 else 'Failed'}")
    
    # Test 2: Direct username authentication (should fail with current setup)
    print("\n2. Testing username authentication:")
    user2 = authenticate(username=admin_user.username, password='admin123')
    print(f"   Result: {'Success' if user2 else 'Failed'}")
    
    # Test 3: What we need for frontend
    print(f"\n3. Frontend should use:")
    print(f"   Email: {admin_user.email}")
    print(f"   Password: admin123")

if __name__ == '__main__':
    test_auth_methods()