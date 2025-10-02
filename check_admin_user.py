#!/usr/bin/env python
"""
Check and create admin user with proper permissions
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def main():
    print("Checking admin users...")
    
    # Check for existing admin users
    admin_users = User.objects.filter(is_staff=True)
    superusers = User.objects.filter(is_superuser=True)
    role_admins = User.objects.filter(role='admin')
    
    print(f"Staff users: {admin_users.count()}")
    print(f"Superusers: {superusers.count()}")
    print(f"Role admins: {role_admins.count()}")
    
    if admin_users.exists():
        for user in admin_users:
            print(f"Staff user: {user.username} - {user.email} - Staff: {user.is_staff} - Super: {user.is_superuser} - Role: {user.role}")
    
    # Update existing admin user
    try:
        admin_user = User.objects.get(username='admin')
        print(f"Found existing admin user: {admin_user.username}")
        
        # Update permissions
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.role = 'admin'
        admin_user.is_active = True
        admin_user.save()
        print("Updated admin user permissions")
        
    except User.DoesNotExist:
        print("No admin user found with username 'admin'")
        # Try to find any staff user and update them
        staff_user = User.objects.filter(is_staff=True).first()
        if staff_user:
            admin_user = staff_user
            admin_user.role = 'admin'
            admin_user.save()
            print(f"Updated staff user {admin_user.username} to admin role")
        else:
            print("No staff users found")
            return
    
    # Verify admin user
    if 'admin_user' in locals():
        admin_user.refresh_from_db()
        print(f"Final admin user status:")
        print(f"  Username: {admin_user.username}")
        print(f"  Email: {admin_user.email}")
        print(f"  is_staff: {admin_user.is_staff}")
        print(f"  is_superuser: {admin_user.is_superuser}")
        print(f"  role: {admin_user.role}")
        print(f"  is_active: {admin_user.is_active}")

if __name__ == "__main__":
    main()