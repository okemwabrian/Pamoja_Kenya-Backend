import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from accounts.models import User

# Create superuser
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@pamojakenyamn.com',
        'first_name': 'Admin',
        'last_name': 'User',
        'is_staff': True,
        'is_superuser': True
    }
)

if created:
    admin_user.set_password('admin123')
    admin_user.save()
    print("Admin user created successfully!")
    print("Username: admin")
    print("Password: admin123")
else:
    print("Admin user already exists")
    print("Username: admin")
    print("Password: admin123")

# Create regular test user
test_user, created = User.objects.get_or_create(
    username='testuser',
    defaults={
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User'
    }
)

if created:
    test_user.set_password('test123')
    test_user.save()
    print("Test user created successfully!")
    print("Username: testuser")
    print("Password: test123")
else:
    print("Test user already exists")
    print("Username: testuser")
    print("Password: test123")