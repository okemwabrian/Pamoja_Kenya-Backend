#!/usr/bin/env python
import os
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from django.conf import settings
from notifications.firebase_email_service import firebase_email_service

def test_firebase_email():
    """Test Firebase email service"""
    print("Testing Firebase Email Service...")
    print(f"Firebase URL: {settings.FIREBASE_EMAIL_FUNCTION_URL}")
    print(f"Use Firebase: {settings.USE_FIREBASE_EMAIL}")
    
    if not settings.FIREBASE_EMAIL_FUNCTION_URL:
        print("❌ Firebase email function URL not configured")
        return False
    
    # Test data
    test_email = {
        'to': 'pamojakeny@gmail.com',
        'subject': 'Test Email from Pamoja Kenya Backend',
        'html': '''
        <h1>🎉 Firebase Email Test</h1>
        <p>Hello from Pamoja Kenya backend!</p>
        <p>This email was sent through Firebase Functions.</p>
        <ul>
            <li>✅ Firebase Functions working</li>
            <li>✅ Email service integrated</li>
            <li>✅ Django backend connected</li>
        </ul>
        <p>Best regards,<br>Pamoja Kenya Development Team</p>
        ''',
        'text': 'Firebase Email Test - Hello from Pamoja Kenya backend! This email was sent through Firebase Functions.'
    }
    
    try:
        # Test direct API call
        print("\n1. Testing direct Firebase Function call...")
        response = requests.post(
            settings.FIREBASE_EMAIL_FUNCTION_URL,
            json=test_email,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Direct Firebase call successful")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Direct Firebase call failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        # Test through Django service
        print("\n2. Testing through Django Firebase service...")
        success = firebase_email_service.send_email(
            test_email['to'],
            test_email['subject'],
            test_email['html'],
            test_email['text']
        )
        
        if success:
            print("✅ Django Firebase service successful")
        else:
            print("❌ Django Firebase service failed")
            return False
        
        print("\n🎉 All tests passed! Firebase email integration is working.")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_application_email():
    """Test application confirmation email"""
    print("\n3. Testing application confirmation email...")
    
    from accounts.models import User
    from applications.models import Application
    
    # Get or create test user
    user, created = User.objects.get_or_create(
        username='testuser_email',
        defaults={
            'email': 'pamojakeny@gmail.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    # Get or create test application
    application, created = Application.objects.get_or_create(
        user=user,
        defaults={
            'application_type': 'single',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'pamojakeny@gmail.com',
            'phone': '123-456-7890',
            'address': '123 Test Street',
            'city': 'Nairobi',
            'state': 'Nairobi',
            'zip_code': '00100',
            'amount': 500.00
        }
    )
    
    # Test application confirmation email
    success = firebase_email_service.send_application_confirmation(user, application)
    
    if success:
        print("✅ Application confirmation email sent successfully")
        return True
    else:
        print("❌ Application confirmation email failed")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("PAMOJA KENYA FIREBASE EMAIL TEST")
    print("=" * 50)
    
    # Test basic email
    basic_test = test_firebase_email()
    
    # Test application email
    app_test = test_application_email()
    
    print("\n" + "=" * 50)
    print("TEST RESULTS:")
    print(f"Basic Email Test: {'✅ PASSED' if basic_test else '❌ FAILED'}")
    print(f"Application Email Test: {'✅ PASSED' if app_test else '❌ FAILED'}")
    print("=" * 50)
    
    if basic_test and app_test:
        print("🎉 ALL TESTS PASSED! Firebase email integration is ready.")
    else:
        print("❌ Some tests failed. Check Firebase Functions deployment.")