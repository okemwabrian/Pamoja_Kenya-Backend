import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from django.contrib.auth import authenticate
from accounts.models import User

# Check admin user details
admin_user = User.objects.get(username='admin')
print(f"Username: {admin_user.username}")
print(f"Email: {admin_user.email}")
print(f"First name: {admin_user.first_name}")
print(f"Last name: {admin_user.last_name}")

# Try authenticating with email
auth_user = authenticate(username=admin_user.email, password='admin123')
if auth_user:
    print("Authentication with email successful!")
else:
    print("Authentication with email failed!")
    
# Reset password and try again
admin_user.set_password('admin123')
admin_user.save()
print("Password reset again...")

auth_user = authenticate(username=admin_user.email, password='admin123')
if auth_user:
    print("Authentication after reset successful!")
else:
    print("Authentication after reset failed!")