#!/usr/bin/env python3

import requests
import json

# Test the simple login endpoint
def test_login():
    url = "http://localhost:8000/api/simple-login/"
    
    # Test credentials
    test_cases = [
        {"username": "admin", "password": "admin123"},
        {"username": "testuser", "password": "test123"},
        {"username": "wrong", "password": "wrong"}
    ]
    
    print("🔌 Testing Backend Login Endpoint")
    print("=" * 50)
    
    for i, credentials in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {credentials['username']}")
        print("-" * 30)
        
        try:
            response = requests.post(url, json=credentials, timeout=5)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ SUCCESS!")
                print(f"User: {data.get('user', {}).get('first_name', 'N/A')} {data.get('user', {}).get('last_name', 'N/A')}")
                print(f"Role: {'Admin' if data.get('user', {}).get('is_staff') else 'User'}")
                print(f"Token: {data.get('access', 'N/A')[:20]}...")
            else:
                print("❌ FAILED!")
                try:
                    error_data = response.json()
                    print(f"Error: {error_data}")
                except:
                    print(f"Error: {response.text}")
                    
        except requests.exceptions.ConnectionError:
            print("❌ CONNECTION FAILED!")
            print("Backend server is not running or not accessible")
            break
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    test_login()