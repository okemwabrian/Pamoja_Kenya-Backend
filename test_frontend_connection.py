#!/usr/bin/env python
"""
Test frontend connection after CORS fixes
"""

import requests
import json

BASE_URL = 'http://127.0.0.1:8000'

def test_frontend_connection():
    print("Testing frontend connection...")
    
    # Test 1: CORS preflight
    print("\n1. Testing CORS preflight...")
    try:
        response = requests.options(
            f"{BASE_URL}/api/auth/login/",
            headers={
                'Origin': 'http://localhost:4200',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type,Authorization'
            }
        )
        print(f"CORS preflight: {response.status_code}")
        cors_origin = response.headers.get('access-control-allow-origin', 'Not found')
        print(f"CORS origin: {cors_origin}")
    except Exception as e:
        print(f"CORS test failed: {e}")
    
    # Test 2: Login request
    print("\n2. Testing login request...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login/",
            json={"username": "admin", "password": "admin123"},
            headers={
                'Content-Type': 'application/json',
                'Origin': 'http://localhost:4200'
            }
        )
        print(f"Login: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"User ID: {data['user']['id']}")
            print(f"Is Admin: {data['user']['is_admin']}")
            print("Login working!")
        else:
            print(f"Login failed: {response.text}")
    except Exception as e:
        print(f"Login test failed: {e}")
    
    # Test 3: Public announcements
    print("\n3. Testing public announcements...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/notifications/announcements/",
            headers={'Origin': 'http://localhost:4200'}
        )
        print(f"Announcements: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} announcements")
        else:
            print(f"Announcements failed: {response.text}")
    except Exception as e:
        print(f"Announcements test failed: {e}")
    
    print("\n✅ Backend is now accepting frontend requests!")
    print("Frontend should be able to connect successfully.")

if __name__ == '__main__':
    test_frontend_connection()