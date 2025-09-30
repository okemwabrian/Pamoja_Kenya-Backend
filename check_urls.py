#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from django.urls import reverse
from django.test import Client

def check_urls():
    print("Checking URL patterns...")
    
    try:
        # Test URL reversing
        login_url = reverse('login')
        print(f"Login URL: {login_url}")
        
        profile_url = reverse('profile')
        print(f"Profile URL: {profile_url}")
        
        stats_url = reverse('user_stats')
        print(f"Stats URL: {stats_url}")
        
    except Exception as e:
        print(f"URL reverse error: {e}")
    
    # Test with client
    client = Client()
    
    # Test login
    response = client.post('/api/auth/login/', {
        'username': 'admin@pamojakenyamn.com',
        'password': 'admin123'
    }, content_type='application/json')
    
    print(f"Login test: {response.status_code}")
    
    if response.status_code == 200:
        import json
        data = json.loads(response.content)
        token = data.get('tokens', {}).get('access')
        
        if token:
            # Test profile with token
            response = client.get('/api/auth/profile/', 
                HTTP_AUTHORIZATION=f'Bearer {token}')
            print(f"Profile test: {response.status_code}")
            
            # Test stats with token
            response = client.get('/api/auth/stats/', 
                HTTP_AUTHORIZATION=f'Bearer {token}')
            print(f"Stats test: {response.status_code}")

if __name__ == '__main__':
    check_urls()