#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from accounts.serializers import UserLoginSerializer
from django.contrib.auth import authenticate

# Test the serializer directly
data = {
    'identifier': 'simpletest@example.com',
    'password': 'simplepass123'
}

serializer = UserLoginSerializer(data=data)
print(f"Serializer data: {data}")
print(f"Is valid: {serializer.is_valid()}")
if not serializer.is_valid():
    print(f"Errors: {serializer.errors}")
else:
    print(f"Validated data: {serializer.validated_data}")

# Test authentication directly
auth_user = authenticate(username='simpletest@example.com', password='simplepass123')
print(f"Direct auth: {auth_user}")

# Test with email field instead
data2 = {
    'email': 'simpletest@example.com',
    'password': 'simplepass123'
}

serializer2 = UserLoginSerializer(data=data2)
print(f"\nWith email field:")
print(f"Is valid: {serializer2.is_valid()}")
if not serializer2.is_valid():
    print(f"Errors: {serializer2.errors}")
else:
    print(f"Validated data: {serializer2.validated_data}")