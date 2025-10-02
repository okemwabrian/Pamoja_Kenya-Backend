from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import Notification, Event, Announcement, Meeting, EventRegistration
from .serializers import NotificationSerializer, EventSerializer, AnnouncementSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def public_announcements(request):
    """Get public announcements (no authentication required)"""
    limit = int(request.GET.get('limit', 10))
    announcements = Announcement.objects.filter(
        is_active=True,
        expires_at__gt=timezone.now()
    ).order_by('-is_pinned', '-created_at')[:limit]
    
    data = []
    for ann in announcements:
        data.append({
            'id': ann.id,
            'title': ann.title,
            'content': ann.content,
            'priority': ann.priority,
            'is_pinned': ann.is_pinned,
            'created_at': ann.created_at.isoformat()
        })
    
    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny])
def public_events(request):
    """Get public events (no authentication required)"""
    limit = int(request.GET.get('limit', 10))
    events = Event.objects.filter(
        is_active=True,
        date__gt=timezone.now()
    ).order_by('date')[:limit]
    
    data = []
    for event in events:
        data.append({
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'date': event.date.isoformat(),
            'location': event.location,
            'is_featured': event.is_featured,
            'registration_required': event.registration_required
        })
    
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_notifications(request):
    """Get user notifications (authentication required)"""
    notifications = Notification.objects.filter(user=request.user)[:20]
    data = []
    for notif in notifications:
        data.append({
            'id': notif.id,
            'title': notif.title,
            'message': notif.message,
            'type': notif.notification_type,
            'is_read': notif.is_read,
            'created_at': notif.created_at.isoformat()
        })
    
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, notification_id):
    """Mark notification as read"""
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return Response({'message': 'Notification marked as read'})
    except Notification.DoesNotExist:
        return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def public_meetings(request):
    """Get public meetings (no authentication required)"""
    limit = int(request.GET.get('limit', 10))
    meetings = Meeting.objects.filter(
        date__gt=timezone.now()
    ).order_by('date')[:limit]
    
    data = []
    for meeting in meetings:
        data.append({
            'id': meeting.id,
            'title': meeting.title,
            'description': meeting.description,
            'date': meeting.date.isoformat(),
            'duration': meeting.duration,
            'type': meeting.type,
            'require_registration': meeting.require_registration
        })
    
    return Response(data)

# Legacy view functions for URL compatibility
@api_view(['GET'])
@permission_classes([AllowAny])
def notifications_list(request):
    return Response([])

@api_view(['GET'])
@permission_classes([AllowAny])
def announcements_list(request):
    return public_announcements(request)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_announcement(request):
    return Response({'message': 'Not implemented'})

@api_view(['GET'])
@permission_classes([AllowAny])
def events_list(request):
    return public_events(request)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event(request):
    return Response({'message': 'Not implemented'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_for_event(request, event_id):
    return Response({'message': 'Not implemented'})

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_contact(request):
    return Response({'message': 'Not implemented'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_contacts_list(request):
    return Response([])

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def admin_update_contact(request, contact_id):
    return Response({'message': 'Not implemented'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_notifications_list(request):
    return Response([])

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_admin_notification(request):
    return Response({'message': 'Not implemented'})