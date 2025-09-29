import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from accounts.models import User
from claims.models import Claim
from notifications.models import Event, Announcement

# Create test user
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User'
    }
)

if created:
    user.set_password('testpass123')
    user.save()
    print("Created test user")

# Create test claims
test_claims = [
    {
        'claim_type': 'death',
        'amount_requested': 5000.00,
        'description': 'Death benefit claim for family member',
        'status': 'pending'
    },
    {
        'claim_type': 'medical',
        'amount_requested': 2500.00,
        'description': 'Medical emergency expenses',
        'status': 'approved',
        'amount_approved': 2500.00
    }
]

for claim_data in test_claims:
    claim, created = Claim.objects.get_or_create(
        user=user,
        claim_type=claim_data['claim_type'],
        defaults=claim_data
    )
    if created:
        print(f"Created {claim_data['claim_type']} claim")

# Create test events
test_events = [
    {
        'title': 'Annual General Meeting',
        'description': 'Join us for our annual general meeting to discuss the year\'s progress and future plans.',
        'date': '2025-10-15 14:00:00',
        'location': 'Community Center, Minneapolis',
        'is_featured': True
    },
    {
        'title': 'Financial Literacy Workshop',
        'description': 'Learn about financial planning and investment strategies.',
        'date': '2025-11-20 18:00:00',
        'location': 'Online via Zoom',
        'registration_required': True
    }
]

for event_data in test_events:
    from datetime import datetime
    event_data['date'] = datetime.strptime(event_data['date'], '%Y-%m-%d %H:%M:%S')
    
    event, created = Event.objects.get_or_create(
        title=event_data['title'],
        defaults={**event_data, 'created_by': user}
    )
    if created:
        print(f"Created event: {event_data['title']}")

# Create test announcements
test_announcements = [
    {
        'title': 'New Benefit Structure',
        'content': 'We are pleased to announce updates to our benefit structure, effective January 2025. All members will receive enhanced coverage.',
        'priority': 'high',
        'is_pinned': True
    },
    {
        'title': 'Holiday Office Hours',
        'content': 'Please note that our offices will have limited hours during the holiday season. Emergency contacts remain available 24/7.',
        'priority': 'medium'
    }
]

for announcement_data in test_announcements:
    announcement, created = Announcement.objects.get_or_create(
        title=announcement_data['title'],
        defaults={**announcement_data, 'created_by': user}
    )
    if created:
        print(f"Created announcement: {announcement_data['title']}")

print("Test data creation completed!")