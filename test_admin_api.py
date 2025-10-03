#!/usr/bin/env python
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Login first to get admin token
def get_admin_token():
    login_data = {
        "identifier": "admin@pamojakenyamn.com",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login/", json=login_data)
    if response.status_code == 200:
        return response.json()['tokens']['access']
    else:
        print(f"Login failed: {response.status_code} - {response.text}")
        return None

def test_admin_endpoints():
    token = get_admin_token()
    if not token:
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test all admin endpoints
    endpoints = [
        ("GET", "/api/admin/stats/", "Admin Stats"),
        ("GET", "/api/admin/users/", "Admin Users"),
        ("GET", "/api/admin/applications/", "Admin Applications"),
        ("GET", "/api/admin/claims/", "Admin Claims"),
        ("GET", "/api/admin/contacts/", "Admin Contacts"),
        ("GET", "/api/notifications/announcements/", "Announcements"),
        ("GET", "/api/notifications/events/", "Events"),
    ]
    
    print("Testing Admin API Endpoints:")
    print("=" * 50)
    
    for method, endpoint, name in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
            status = "✅ PASS" if response.status_code == 200 else f"❌ FAIL ({response.status_code})"
            print(f"{name:<20} {endpoint:<30} {status}")
            
            if response.status_code != 200:
                print(f"  Error: {response.text[:100]}...")
                
        except Exception as e:
            print(f"{name:<20} {endpoint:<30} ❌ ERROR: {str(e)}")
    
    print("=" * 50)

if __name__ == "__main__":
    test_admin_endpoints()