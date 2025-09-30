from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from applications.models import Application
from claims.models import Claim
from notifications.models import Event, Announcement, Notification
from payments.models import Payment

User = get_user_model()

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def admin_dashboard_stats(request):
    """Get admin dashboard statistics"""
    stats = {
        'total_users': User.objects.count(),
        'total_applications': Application.objects.count(),
        'pending_applications': Application.objects.filter(status='pending').count(),
        'approved_applications': Application.objects.filter(status='approved').count(),
        'total_claims': Claim.objects.count(),
        'pending_claims': Claim.objects.filter(status='pending').count(),
        'total_payments': Payment.objects.aggregate(total=Sum('amount'))['total'] or 0,
        'active_events': Event.objects.filter(is_active=True).count(),
        'total_announcements': Announcement.objects.filter(is_active=True).count(),
    }
    return Response(stats)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def recent_activities(request):
    """Get recent admin activities"""
    activities = []
    
    # Recent applications
    recent_apps = Application.objects.order_by('-created_at')[:5]
    for app in recent_apps:
        activities.append({
            'id': app.id,
            'type': 'application',
            'title': f'New {app.application_type} application',
            'description': f'{app.first_name} {app.last_name} submitted application',
            'date': app.created_at.isoformat(),
            'status': app.status,
            'user': f'{app.first_name} {app.last_name}'
        })
    
    # Recent claims
    recent_claims = Claim.objects.order_by('-created_at')[:5]
    for claim in recent_claims:
        activities.append({
            'id': claim.id,
            'type': 'claim',
            'title': f'{claim.get_claim_type_display()} claim',
            'description': f'${claim.amount_requested} claim submitted',
            'date': claim.created_at.isoformat(),
            'status': claim.status,
            'user': claim.user.username if claim.user else 'Unknown'
        })
    
    # Sort by date
    activities.sort(key=lambda x: x['date'], reverse=True)
    
    return Response(activities[:10])

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def users_list(request):
    """Get list of all users"""
    users = User.objects.all().order_by('-date_joined')
    users_data = []
    
    for user in users:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'date_joined': user.date_joined.strftime('%Y-%m-%d'),
            'applications_count': user.applications.count(),
            'claims_count': user.claims.count() if hasattr(user, 'claims') else 0
        })
    
    return Response(users_data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def applications_list(request):
    """Get list of all applications"""
    applications = Application.objects.all().order_by('-created_at')
    apps_data = []
    
    for app in applications:
        apps_data.append({
            'id': app.id,
            'applicant': f'{app.first_name} {app.last_name}',
            'email': app.email,
            'type': app.application_type,
            'status': app.status,
            'amount': str(app.amount),
            'created_at': app.created_at.strftime('%Y-%m-%d %H:%M'),
            'phone': app.phone,
            'city': app.city,
            'state': app.state
        })
    
    return Response(apps_data)

@api_view(['POST'])
@permission_classes([AllowAny])
def update_application_status(request, app_id):
    """Update application status"""
    try:
        application = Application.objects.get(id=app_id)
        new_status = request.data.get('status')
        admin_notes = request.data.get('admin_notes', '')
        
        if new_status in ['pending', 'approved', 'rejected']:
            application.status = new_status
            application.admin_notes = admin_notes
            application.save()
            
            # Create notification for user
            if hasattr(application, 'user') and application.user:
                Notification.objects.create(
                    user=application.user,
                    title=f'Application {new_status.title()}',
                    message=f'Your {application.application_type} application has been {new_status}.',
                    notification_type=f'application_{new_status}'
                )
            
            return Response({'message': f'Application {new_status} successfully'})
        else:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
            
    except Application.DoesNotExist:
        return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_announcement(request):
    """Create new announcement"""
    data = request.data
    
    # Get admin user or create mock admin
    admin_user = request.user if request.user.is_authenticated else User.objects.filter(is_staff=True).first()
    if not admin_user:
        admin_user = User.objects.create_user(username='admin', email='admin@example.com', is_staff=True)
    
    announcement = Announcement.objects.create(
        title=data.get('title'),
        content=data.get('content'),
        priority=data.get('priority', 'medium'),
        is_pinned=data.get('is_pinned', False),
        expires_at=data.get('expires_at'),
        created_by=admin_user
    )
    
    # Create notifications for high priority announcements
    if announcement.priority in ['high', 'urgent']:
        users = User.objects.filter(is_active=True)
        notifications = []
        
        for user in users:
            notifications.append(Notification(
                user=user,
                title=f'Important: {announcement.title}',
                message=announcement.content[:200] + '...' if len(announcement.content) > 200 else announcement.content,
                notification_type='announcement'
            ))
        
        Notification.objects.bulk_create(notifications)
    
    return Response({
        'id': announcement.id,
        'message': 'Announcement created successfully'
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_event(request):
    """Create new event"""
    data = request.data
    
    # Get admin user or create mock admin
    admin_user = request.user if request.user.is_authenticated else User.objects.filter(is_staff=True).first()
    if not admin_user:
        admin_user = User.objects.create_user(username='admin', email='admin@example.com', is_staff=True)
    
    event = Event.objects.create(
        title=data.get('title'),
        description=data.get('description'),
        date=data.get('date'),
        end_date=data.get('end_date'),
        location=data.get('location', ''),
        is_featured=data.get('is_featured', False),
        registration_required=data.get('registration_required', False),
        max_attendees=data.get('max_attendees'),
        created_by=admin_user
    )
    
    # Create notifications for all users
    users = User.objects.filter(is_active=True)
    notifications = []
    
    for user in users:
        notifications.append(Notification(
            user=user,
            title='New Event Created',
            message=f'New event "{event.title}" scheduled for {event.date.strftime("%B %d, %Y")}.',
            notification_type='event_created'
        ))
    
    Notification.objects.bulk_create(notifications)
    
    return Response({
        'id': event.id,
        'message': 'Event created successfully'
    }, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdminUser])
def user_detail(request, user_id):
    """Get, update, or delete user"""
    try:
        user = User.objects.get(id=user_id)
        
        if request.method == 'GET':
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'date_joined': user.date_joined.isoformat(),
                'membership_status': getattr(user, 'membership_status', 'active')
            })
        
        elif request.method == 'PATCH':
            # Update user fields
            for field in ['first_name', 'last_name', 'email', 'is_active', 'is_staff']:
                if field in request.data:
                    setattr(user, field, request.data[field])
            user.save()
            return Response({'message': 'User updated successfully'})
        
        elif request.method == 'DELETE':
            user.delete()
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)