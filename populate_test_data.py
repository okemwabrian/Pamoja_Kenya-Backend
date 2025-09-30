#!/usr/bin/env python
import os
import django
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from accounts.models import User
from applications.models import Application
from payments.models import Payment
from beneficiaries.models import Beneficiary, BeneficiaryChangeRequest
from claims.models import Claim, Beneficiary as ClaimBeneficiary, BenefitPayment
from notifications.models import Notification, Event, Announcement, EventRegistration

def create_test_data():
    print("Creating test data...")
    
    # Create test users
    users = []
    for i in range(5):
        user, created = User.objects.get_or_create(
            username=f'testuser{i+1}',
            defaults={
                'email': f'testuser{i+1}@example.com',
                'first_name': f'Test{i+1}',
                'last_name': 'User',
                'phone': f'123-456-789{i}',
                'address': f'{i+1}23 Test Street',
                'city': 'Nairobi',
                'state': 'Nairobi',
                'zip_code': f'0010{i}',
                'role': 'user',
                'membership_status': 'active' if i % 2 == 0 else 'pending'
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
        users.append(user)
        print(f"Created user: {user.username}")
    
    # Create applications
    app_types = ['single', 'double']
    statuses = ['pending', 'approved', 'rejected']
    
    for i, user in enumerate(users):
        app, created = Application.objects.get_or_create(
            user=user,
            defaults={
                'application_type': app_types[i % 2],
                'status': statuses[i % 3],
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': user.phone,
                'date_of_birth': datetime(1990 + i, 1, 15).date(),
                'address': user.address,
                'city': user.city,
                'state': user.state,
                'zip_code': user.zip_code,
                'country': 'Kenya',
                'emergency_contact_name': f'Emergency Contact {i+1}',
                'emergency_contact_phone': f'987-654-321{i}',
                'emergency_contact_relationship': 'Spouse',
                'occupation': f'Job Title {i+1}',
                'employer': f'Company {i+1}',
                'annual_income': Decimal(50000 + (i * 10000)),
                'amount': Decimal(500 + (i * 100)),
                'notes': f'Test application notes for user {i+1}'
            }
        )
        if created:
            print(f"Created application for: {user.username}")
    
    # Create payments
    payment_methods = ['paypal', 'stripe', 'mpesa', 'bank_transfer']
    payment_statuses = ['pending', 'completed', 'failed']
    
    applications = Application.objects.all()
    for i, app in enumerate(applications[:3]):
        payment, created = Payment.objects.get_or_create(
            user=app.user,
            application=app,
            defaults={
                'amount': app.amount,
                'currency': 'USD',
                'payment_method': payment_methods[i % 4],
                'status': payment_statuses[i % 3],
                'payer_name': f"{app.first_name} {app.last_name}",
                'payer_email': app.email,
                'description': f'Payment for {app.get_application_type_display()} application',
                'transaction_id': f'TXN{1000 + i}'
            }
        )
        if created:
            print(f"Created payment for: {app.user.username}")
    
    # Create beneficiaries
    relationships = ['Spouse', 'Child', 'Parent', 'Sibling']
    for i, user in enumerate(users):
        beneficiary, created = Beneficiary.objects.get_or_create(
            user=user,
            name=f'Beneficiary {i+1}',
            defaults={
                'relationship': relationships[i % 4],
                'email': f'beneficiary{i+1}@example.com',
                'phone': f'555-000-{i+1}00',
                'date_of_birth': datetime(1995 + i, 6, 10).date(),
                'address': f'{i+1}45 Beneficiary Street',
                'city': 'Mombasa',
                'state': 'Mombasa',
                'zip_code': f'8010{i}',
                'country': 'Kenya',
                'percentage': Decimal(100.00) if i % 2 == 0 else Decimal(50.00),
                'is_primary': i % 2 == 0,
                'notes': f'Test beneficiary notes for {user.username}'
            }
        )
        if created:
            print(f"Created beneficiary for: {user.username}")
    
    # Create claims
    claim_types = ['death', 'medical', 'education', 'emergency']
    claim_statuses = ['pending', 'approved', 'rejected', 'paid']
    
    for i, user in enumerate(users):
        claim, created = Claim.objects.get_or_create(
            user=user,
            defaults={
                'claim_type': claim_types[i % 4],
                'amount_requested': Decimal(1000 + (i * 500)),
                'description': f'Test {claim_types[i % 4]} claim for user {user.username}',
                'status': claim_statuses[i % 4]
            }
        )
        if created:
            if claim.status == 'approved':
                claim.amount_approved = claim.amount_requested
                claim.save()
            print(f"Created claim for: {user.username}")
    
    # Create notifications
    notification_types = ['application_submitted', 'application_approved', 'payment_received', 'claim_submitted']
    
    for i, user in enumerate(users):
        notification, created = Notification.objects.get_or_create(
            user=user,
            title=f'Test Notification {i+1}',
            defaults={
                'message': f'This is a test notification for {user.username}',
                'notification_type': notification_types[i % 4],
                'is_read': i % 2 == 0
            }
        )
        if created:
            print(f"Created notification for: {user.username}")
    
    # Create events
    admin_user = User.objects.filter(is_superuser=True).first()
    if admin_user:
        for i in range(3):
            event, created = Event.objects.get_or_create(
                title=f'Test Event {i+1}',
                defaults={
                    'description': f'This is test event {i+1} description',
                    'date': timezone.now() + timedelta(days=i*7),
                    'end_date': timezone.now() + timedelta(days=i*7, hours=2),
                    'location': f'Test Venue {i+1}, Nairobi',
                    'is_active': True,
                    'is_featured': i == 0,
                    'registration_required': True,
                    'max_attendees': 50 + (i * 25),
                    'created_by': admin_user
                }
            )
            if created:
                print(f"Created event: {event.title}")
    
    # Create announcements
    priorities = ['low', 'medium', 'high', 'urgent']
    if admin_user:
        for i in range(4):
            announcement, created = Announcement.objects.get_or_create(
                title=f'Test Announcement {i+1}',
                defaults={
                    'content': f'This is test announcement {i+1} content with important information.',
                    'priority': priorities[i],
                    'is_active': True,
                    'is_pinned': i < 2,
                    'expires_at': timezone.now() + timedelta(days=30) if i % 2 == 0 else None,
                    'created_by': admin_user
                }
            )
            if created:
                print(f"Created announcement: {announcement.title}")
    
    print("Test data creation completed!")

if __name__ == '__main__':
    create_test_data()