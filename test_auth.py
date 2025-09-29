import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from django.contrib.auth import authenticate
from accounts.models import User

# Test user existence
try:
    admin_user = User.objects.get(username='admin')
    print(f"Admin user found: {admin_user.username}")
    print(f"Is staff: {admin_user.is_staff}")
    print(f"Is active: {admin_user.is_active}")
    print(f"Password set: {admin_user.has_usable_password()}")
    
    # Test authentication
    auth_user = authenticate(username='admin', password='admin123')
    if auth_user:
        print("Authentication successful!")
    else:
        print("Authentication failed!")
        
except User.DoesNotExist:
    print("Admin user not found!")
    
# List all users
print("\nAll users:")
for user in User.objects.all():
    print(f"- {user.username} (staff: {user.is_staff}, active: {user.is_active})")