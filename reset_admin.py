import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from accounts.models import User

# Reset admin password
try:
    admin_user = User.objects.get(username='admin')
    admin_user.set_password('admin123')
    admin_user.save()
    print("Admin password reset successfully!")
    
    # Test authentication
    from django.contrib.auth import authenticate
    auth_user = authenticate(username='admin', password='admin123')
    if auth_user:
        print("Authentication test successful!")
    else:
        print("Authentication test failed!")
        
except User.DoesNotExist:
    print("Admin user not found!")