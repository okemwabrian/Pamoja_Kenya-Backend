#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import json

@csrf_exempt
@require_http_methods(["POST"])
def simple_login(request):
    try:
        data = json.loads(request.body)
        identifier = data.get('identifier') or data.get('email')
        password = data.get('password')
        
        print(f"Login attempt - identifier: {identifier}, password: {'*' * len(password) if password else 'None'}")
        
        if not identifier or not password:
            return JsonResponse({'error': 'Email and password required'}, status=400)
        
        # Authenticate user
        user = authenticate(username=identifier, password=password)
        print(f"Authentication result: {user}")
        
        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
            
    except Exception as e:
        print(f"Login error: {e}")
        return JsonResponse({'error': 'Server error'}, status=500)

if __name__ == "__main__":
    # Test the function directly
    from django.test import RequestFactory
    
    factory = RequestFactory()
    request_data = json.dumps({
        'identifier': 'simpletest@example.com',
        'password': 'simplepass123'
    })
    
    request = factory.post('/test-login/', request_data, content_type='application/json')
    response = simple_login(request)
    
    print(f"Response status: {response.status_code}")
    print(f"Response content: {response.content.decode()}")