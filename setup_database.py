#!/usr/bin/env python
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model

def setup_database():
    print("Setting up Pamoja Kenya Database...")
    print("=" * 50)
    
    try:
        # Create migrations
        print("Creating migrations...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        
        # Apply migrations
        print("Applying migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Create superuser
        User = get_user_model()
        
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@pamojakenyamn.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                role='admin',
                is_staff=True,
                is_superuser=True,
                membership_status='active'
            )
            print("✅ Admin user created: admin / admin123")
        else:
            print("✅ Admin user already exists")
        
        # Create test user
        if not User.objects.filter(username='testuser').exists():
            test_user = User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='test123',
                first_name='Test',
                last_name='User',
                role='user',
                membership_status='active'
            )
            print("✅ Test user created: testuser / test123")
        else:
            print("✅ Test user already exists")
        
        print("=" * 50)
        print("✅ Database setup complete!")
        print("🚀 You can now start the server with: python manage.py runserver")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        sys.exit(1)

if __name__ == '__main__':
    setup_database()