#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
django.setup()

from django.utils import timezone
from accounts.models import User
from notifications.models import Announcement, Event

def create_announcements():
    admin_user = User.objects.filter(is_staff=True).first()
    if not admin_user:
        print("No admin user found")
        return
    
    # Create announcements
    announcements = [
        {
            'title': 'Welcome to Pamoja Kenya MN',
            'content': 'Welcome to our community platform. Stay connected with fellow members and get the latest updates on events and activities.',
            'priority': 'high',
            'is_pinned': True
        },
        {
            'title': 'Monthly Community Meeting',
            'content': 'Join us for our monthly community meeting this Saturday at 2 PM. We will discuss upcoming events and community initiatives.',
            'priority': 'medium',
            'is_pinned': False
        },
        {
            'title': 'New Member Registration Open',
            'content': 'We are now accepting new member applications. Single family membership is $200 and double family membership is $400.',
            'priority': 'medium',
            'is_pinned': False
        }
    ]
    
    for ann_data in announcements:
        announcement, created = Announcement.objects.get_or_create(
            title=ann_data['title'],
            defaults={
                'content': ann_data['content'],
                'priority': ann_data['priority'],
                'is_active': True,
                'is_pinned': ann_data['is_pinned'],
                'created_by': admin_user,
                'expires_at': timezone.now() + timedelta(days=30)
            }
        )
        if created:
            print(f"Created announcement: {ann_data['title']}")
    
    # Create events
    events = [
        {
            'title': 'Community Picnic',
            'description': 'Join us for a fun-filled community picnic with food, games, and entertainment for the whole family.',
            'location': 'Central Park',
            'is_featured': True
        },
        {
            'title': 'Cultural Night',
            'description': 'Celebrate our rich Kenyan culture with traditional music, dance, and food.',
            'location': 'Community Center',
            'is_featured': False
        }
    ]
    
    for event_data in events:
        event, created = Event.objects.get_or_create(
            title=event_data['title'],
            defaults={
                'description': event_data['description'],
                'date': timezone.now() + timedelta(days=14),
                'location': event_data['location'],
                'is_active': True,
                'is_featured': event_data['is_featured'],
                'registration_required': True,
                'created_by': admin_user
            }
        )
        if created:
            print(f"Created event: {event_data['title']}")
    
    print("Test data creation complete!")

if __name__ == '__main__':
    create_announcements()