from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from django.utils import timezone
from .models import Notification, Event, Announcement, EventRegistration

@api_view(['GET'])
@permission_classes([AllowAny])
def user_notifications(request):
    """Get notifications for current user"""
    # Mock notifications for testing
    notifications = [
        {
            'id': 1,
            'title': 'Welcome to Pamoja Kenya MN',
            'message': 'Thank you for joining our community!',
            'is_read': False,
            'created_at': '2025-09-28T10:00:00Z'
        },
        {
            'id': 2,
            'title': 'Application Update',
            'message': 'Your membership application has been approved.',
            'is_read': False,
            'created_at': '2025-09-27T15:30:00Z'
        }
    ]
    
    return Response(notifications)

@api_view(['GET'])
@permission_classes([AllowAny])
def events_list(request):
    """Get list of events"""
    # Mock events for testing
    events = [
        {
            'id': 1,
            'title': 'Annual General Meeting',
            'description': 'Join us for our annual general meeting.',
            'date': '2025-10-15T14:00:00Z',
            'location': 'Community Center',
            'is_featured': True,
            'registration_required': True
        },
        {
            'id': 2,
            'title': 'Financial Literacy Workshop',
            'description': 'Learn about financial planning.',
            'date': '2025-11-20T18:00:00Z',
            'location': 'Online via Zoom',
            'is_featured': False,
            'registration_required': True
        }
    ]
    
    return Response(events)

@api_view(['GET'])
@permission_classes([AllowAny])
def announcements_list(request):
    """Get list of announcements"""
    # Mock announcements for testing
    announcements = [
        {
            'id': 1,
            'title': 'New Benefit Structure',
            'content': 'We are pleased to announce updates to our benefit structure.',
            'priority': 'high',
            'is_pinned': True,
            'created_at': '2025-09-25T09:00:00Z'
        },
        {
            'id': 2,
            'title': 'Holiday Office Hours',
            'content': 'Please note limited hours during the holiday season.',
            'priority': 'medium',
            'is_pinned': False,
            'created_at': '2025-09-20T12:00:00Z'
        }
    ]
    
    return Response(announcements)

@api_view(['POST'])
@permission_classes([AllowAny])
def mark_notification_read(request, notification_id):
    """Mark notification as read"""
    return Response({'message': 'Notification marked as read'})

@api_view(['GET'])
@permission_classes([AllowAny])
def notifications_list(request):
    """Get notifications list"""
    # Mock notifications for testing
    notifications = [
        {
            'id': 1,
            'title': 'Welcome to Pamoja Kenya MN',
            'message': 'Thank you for joining our community!',
            'is_read': False,
            'created_at': '2025-09-28T10:00:00Z'
        },
        {
            'id': 2,
            'title': 'Application Update',
            'message': 'Your membership application has been approved.',
            'is_read': False,
            'created_at': '2025-09-27T15:30:00Z'
        }
    ]
    
    return Response(notifications)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_for_event(request, event_id):
    """Register user for an event"""
    try:
        event = Event.objects.get(id=event_id)
        registration, created = EventRegistration.objects.get_or_create(
            user=request.user,
            event=event
        )
        
        if created:
            return Response({'message': 'Successfully registered for event'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Already registered for this event'}, status=status.HTTP_200_OK)
            
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_announcement(request):
    """Create new announcement (admin only)"""
    data = request.data
    announcement = Announcement.objects.create(
        title=data.get('title'),
        content=data.get('content'),
        priority=data.get('priority', 'medium'),
        is_pinned=data.get('is_pinned', False)
    )
    return Response({
        'id': announcement.id,
        'title': announcement.title,
        'content': announcement.content,
        'priority': announcement.priority,
        'is_pinned': announcement.is_pinned,
        'created_at': announcement.created_at
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_event(request):
    """Create new event (admin only)"""
    data = request.data
    event = Event.objects.create(
        title=data.get('title'),
        description=data.get('description'),
        date=data.get('date'),
        location=data.get('location'),
        is_featured=data.get('is_featured', False),
        registration_required=data.get('registration_required', True)
    )
    return Response({
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'date': event.date,
        'location': event.location,
        'is_featured': event.is_featured,
        'registration_required': event.registration_required
    }, status=status.HTTP_201_CREATED)