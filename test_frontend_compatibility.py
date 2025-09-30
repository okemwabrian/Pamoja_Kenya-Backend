#!/usr/bin/env python
import requests
import json

BASE_URL = 'http://localhost:8000'

def test_endpoint(method, endpoint, data=None, token=None):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    headers = {'Content-Type': 'application/json'}
    
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=headers)
        elif method == 'PATCH':
            response = requests.patch(url, json=data, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        
        if response.content:
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, {'text': response.text}
        else:
            return response.status_code, {'message': 'Empty response'}
    except Exception as e:
        return 0, {'error': str(e)}

def main():
    print("FRONTEND COMPATIBILITY TEST")
    print("=" * 50)
    
    # Test login first
    print("\n1. Testing Authentication...")
    status_code, response = test_endpoint('POST', '/api/auth/login/', {
        'username': 'admin@pamojakenyamn.com',
        'password': 'admin123'
    })
    
    if status_code == 200 and 'access' in response:
        token = response['access']
        print("Login successful")
    else:
        print(f"Login failed: {status_code} - {response}")
        return
    
    # Test all required endpoints
    endpoints = [
        # Authentication
        ('GET', '/api/auth/profile/', None),
        ('GET', '/api/auth/stats/', None),
        ('POST', '/api/auth/password-reset/', {'email': 'test@example.com'}),
        ('POST', '/api/auth/contact/', {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test',
            'message': 'Test message'
        }),
        
        # Applications
        ('GET', '/api/applications/my-applications/', None),
        
        # Payments
        ('GET', '/api/payments/', None),
        
        # Events & Announcements
        ('GET', '/api/notifications/events/', None),
        ('GET', '/api/notifications/announcements/', None),
        
        # Admin
        ('GET', '/api/admin/stats/', None),
        ('GET', '/api/admin/users/', None),
    ]
    
    print(f"\n2. Testing {len(endpoints)} endpoints...")
    
    passed = 0
    failed = 0
    
    for method, endpoint, data in endpoints:
        use_token = not endpoint.startswith('/api/auth/password-reset/') and not endpoint.startswith('/api/auth/contact/')
        status_code, response = test_endpoint(method, endpoint, data, token if use_token else None)
        
        if 200 <= status_code < 300:
            print(f"[OK] {method} {endpoint}")
            passed += 1
        else:
            print(f"[FAIL] {method} {endpoint} - {status_code}: {response.get('error', 'Unknown error')}")
            failed += 1
    
    print(f"\nRESULTS:")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        print("\nALL TESTS PASSED! Frontend integration ready.")
    else:
        print(f"\nWARNING: {failed} endpoints need attention.")

if __name__ == '__main__':
    main()