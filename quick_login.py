#!/usr/bin/env python
import requests
import json

# Try existing users first
LOGIN_OPTIONS = [
    {"identifier": "ken@gmail.com", "password": "password123"},
    {"identifier": "james@mail.com", "password": "password123"},
    {"identifier": "admin@pamojakenyamn.com", "password": "admin123"}
]

def quick_login():
    url = "http://127.0.0.1:8000/api/auth/login/"
    
    for i, login_data in enumerate(LOGIN_OPTIONS):
        print(f"Trying login {i+1}: {login_data['identifier']}")
        
        try:
            response = requests.post(url, json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                print("Login successful!")
                print(f"User: {data['user']['username']}")
                print(f"Email: {data['user']['email']}")
                print(f"Access Token: {data['tokens']['access'][:50]}...")
                return data['tokens']['access']
            else:
                print(f"Failed: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("Server not running. Start with: python manage.py runserver")
            return None
        except Exception as e:
            print(f"Error: {e}")
    
    print("All login attempts failed")
    return None

if __name__ == "__main__":
    quick_login()