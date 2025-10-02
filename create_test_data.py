#!/usr/bin/env python
"""
Create test data for backend verification
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from django.utils import timezone
from accounts.models import User
from applications.models import Application
from payments.models import Payment
from claims.models import Claim
from beneficiaries.models import Beneficiary
from notifications.models import Announcement, Event

def create_test_data():
    """Create test data for verification"""
    print("Creating test data...")
    
    # Create test users
    admin_user, created = User.objects.get_or_create(
        email='admin@pamojakenyamn.com',
        defaults={
            'username': 'admin',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("Admin user created")
    
    test_user, created = User.objects.get_or_create(
        email='test@example.com',
        defaults={
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    if created:
        test_user.set_password('test123')
        test_user.save()
        print("Test user created")
    
    # Create test application
    application, created = Application.objects.get_or_create(
        user=test_user,
        email='test@example.com',
        defaults={
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '123-456-7890',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'MN',
            'zip_code': '12345',
            'application_type': 'single',
            'amount': 200,
            'spouse_name': 'Test Spouse',
            'child_1': 'Test Child 1',
            'parent_1': 'Test Parent 1',
            'sibling_1': 'Test Sibling 1',
            'status': 'pending'
        }
    )
    if created:
        print("Test application created")
    
    # Create test payment
    payment, created = Payment.objects.get_or_create(
        user=test_user,
        defaults={
            'amount': 200.00,
            'payment_method': 'paypal',
            'payer_name': 'Test User',
            'payer_email': 'test@example.com',
            'transaction_id': 'TEST123456',
            'status': 'completed'
        }
    )
    if created:
        print("Test payment created")
    
    # Create test beneficiary
    beneficiary, created = Beneficiary.objects.get_or_create(
        user=test_user,
        defaults={
            'full_name': 'Test Beneficiary',
            'relationship': 'spouse',
            'date_of_birth': '1990-01-01',
            'phone': '123-456-7890',
            'email': 'beneficiary@example.com'
        }
    )
    if created:
        print("Test beneficiary created")
    
    # Create test announcement
    announcement, created = Announcement.objects.get_or_create(
        title='Welcome to Pamoja Kenya',
        defaults={
            'content': 'Welcome to our community platform. Stay updated with the latest news and events.',
            'priority': 'medium',
            'is_active': True,
            'is_pinned': True,
            'created_by': admin_user,
            'expires_at': timezone.now() + timedelta(days=30)
        }
    )
    if created:
        print("Test announcement created")
    
    # Create test event
    event, created = Event.objects.get_or_create(
        title='Community Meeting',
        defaults={
            'description': 'Monthly community meeting to discuss important matters.',
            'date': timezone.now() + timedelta(days=7),
            'location': 'Community Center',
            'is_active': True,
            'is_featured': True,
            'registration_required': True,
            'created_by': admin_user
        }
    )
    if created:
        print("Test event created")
    
    print("Test data creation complete!")

if __name__ == '__main__':
    create_test_data()