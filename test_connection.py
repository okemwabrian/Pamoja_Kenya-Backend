#!/usr/bin/env python
"""
Test frontend-backend connection
"""

import requests
import json

BASE_URL = 'http://127.0.0.1:8000'

def test_connection():
    print("Testing backend connection...")
    
    # Test 1: Basic API root
    try:
        response = requests.get(f"{BASE_URL}/api/")
        print(f"API Root: {response.status_code}")
    except Exception as e:
        print(f"API Root failed: {e}")
    
    # Test 2: Public announcements
    try:
        response = requests.get(f"{BASE_URL}/api/notifications/announcements/")
        if response.status_code == 200:
            data = response.json()
            print(f"Announcements: {response.status_code} - {len(data)} items")
        else:
            print(f"Announcements failed: {response.status_code}")
    except Exception as e:
        print(f"Announcements error: {e}")
    
    # Test 3: CORS headers
    try:
        response = requests.options(f"{BASE_URL}/api/notifications/announcements/", 
                                  headers={'Origin': 'http://localhost:4200'})
        cors_headers = response.headers.get('Access-Control-Allow-Origin', 'Not found')
        print(f"CORS headers: {cors_headers}")
    except Exception as e:
        print(f"CORS test error: {e}")
    
    # Test 4: Login endpoint
    try:
        login_data = {"username": "admin", "password": "admin123"}
        response = requests.post(f"{BASE_URL}/api/auth/login/", 
                               json=login_data,
                               headers={'Content-Type': 'application/json'})
        print(f"Login: {response.status_code}")
        if response.status_code == 200:
            print("✅ Backend is ready for frontend connection")
        else:
            print("❌ Login failed")
    except Exception as e:
        print(f"Login error: {e}")

if __name__ == '__main__':
    test_connection()