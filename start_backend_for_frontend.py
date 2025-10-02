#!/usr/bin/env python
"""
Start Django backend server for frontend connection
"""
import os
import sys
import django
import subprocess
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

def check_database():
    """Check if database is properly set up"""
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Check if admin user exists
        admin_exists = User.objects.filter(is_staff=True).exists()
        total_users = User.objects.count()
        
        print(f"Database Status:")
        print(f"  - Total users: {total_users}")
        print(f"  - Admin user exists: {admin_exists}")
        
        if not admin_exists:
            print("  - Creating admin user...")
            User.objects.create_superuser(
                username='admin',
                email='admin@pamojakenyamn.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            print("  - Admin user created successfully")
        
        return True
    except Exception as e:
        print(f"Database error: {e}")
        return False

def check_required_endpoints():
    """Check if all required endpoints exist"""
    from django.urls import reverse
    from django.test import Client
    
    client = Client()
    endpoints = [
        '/api/auth/login/',
        '/api/auth/register/',
        '/api/applications/my-applications/',
        '/api/claims/',
        '/api/payments/',
        '/api/notifications/list/',
        '/api/admin/stats/',
        '/api/admin/users/',
        '/api/admin/applications/',
        '/api/admin/claims/',
    ]
    
    print("Checking endpoints:")
    for endpoint in endpoints:
        try:
            response = client.get(endpoint)
            status = "[OK]" if response.status_code in [200, 401, 403] else "[FAIL]"
            print(f"  {status} {endpoint} - {response.status_code}")
        except Exception as e:
            print(f"  [ERROR] {endpoint} - Error: {e}")

def main():
    print("=" * 50)
    print("PAMOJA KENYA BACKEND STARTUP")
    print("=" * 50)
    
    # Check database
    if not check_database():
        print("❌ Database check failed")
        return
    
    # Check endpoints
    check_required_endpoints()
    
    print("\n" + "=" * 50)
    print("STARTING DJANGO SERVER")
    print("=" * 50)
    print("Backend will be available at: http://localhost:8000")
    print("Frontend should connect to: http://localhost:8000/api/")
    print("Admin endpoints: http://localhost:8000/api/admin/")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start Django development server
    try:
        subprocess.run([
            sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'
        ], check=True)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    main()