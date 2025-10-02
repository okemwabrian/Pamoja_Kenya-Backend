from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from applications.models import Application
from claims.models import Claim
from notifications.models import Event, Announcement, Notification, Meeting
from payments.models import Payment
from .permissions import IsAdminOrStaff

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAdminOrStaff])
def admin_dashboard_stats(request):
    """Get admin dashboard statistics"""
    stats = {
        'total_users': User.objects.count(),
        'total_applications': Application.objects.count(),
        'pending_applications': Application.objects.filter(status='pending').count(),
        'approved_applications': Application.objects.filter(status='approved').count(),
        'rejected_applications': Application.objects.filter(status='rejected').count(),
        'total_claims': Claim.objects.count(),
        'pending_claims': Claim.objects.filter(status='pending').count(),
        'approved_claims': Claim.objects.filter(status='approved').count(),
        'rejected_claims': Claim.objects.filter(status='rejected').count(),
        'total_payments': Payment.objects.count(),
        'total_revenue': float(Payment.objects.aggregate(total=Sum('amount'))['total'] or 0),
    }
    return Response(stats)

@api_view(['GET'])
@permission_classes([IsAdminOrStaff])
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
@permission_classes([IsAdminOrStaff])
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
@permission_classes([IsAdminOrStaff])
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
@permission_classes([IsAdminOrStaff])
def update_application_status(request, app_id):
    """Update application status"""
    try:
        application = Application.objects.get(id=app_id)
        new_status = request.data.get('status')
        admin_notes = request.data.get('admin_notes', '')
        
        if new_status in ['pending', 'approved', 'rejected']:
            application.status = new_status
            if hasattr(application, 'admin_notes'):
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
@permission_classes([IsAdminOrStaff])
def create_announcement(request):
    """Create new announcement"""
    data = request.data
    
    announcement = Announcement.objects.create(
        title=data.get('title'),
        content=data.get('content'),
        priority=data.get('priority', 'medium'),
        is_pinned=data.get('is_pinned', False),
        expires_at=data.get('expires_at'),
        created_by=request.user
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
@permission_classes([IsAdminOrStaff])
def create_event(request):
    """Create new event"""
    data = request.data
    
    event = Event.objects.create(
        title=data.get('title'),
        description=data.get('description'),
        date=data.get('date'),
        end_date=data.get('end_date'),
        location=data.get('location', ''),
        is_featured=data.get('is_featured', False),
        registration_required=data.get('registration_required', False),
        max_attendees=data.get('max_attendees'),
        created_by=request.user
    )
    
    # Create notifications for all users
    users = User.objects.filter(is_active=True)
    notifications = []
    
    for user in users:
        notifications.append(Notification(
            user=user,
            title='New Event Created',
            message=f'New event "{event.title}" has been created.',
            notification_type='event_created'
        ))
    
    Notification.objects.bulk_create(notifications)
    
    return Response({
        'id': event.id,
        'message': 'Event created successfully'
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAdminOrStaff])
def create_meeting(request):
    """Create new meeting"""
    data = request.data
    
    meeting = Meeting.objects.create(
        title=data.get('title'),
        description=data.get('description'),
        date=data.get('date'),
        duration=data.get('duration', 60),
        type=data.get('type'),
        max_participants=data.get('max_participants'),
        meeting_link=data.get('meeting_link', ''),
        require_registration=data.get('require_registration', False),
        send_notifications=data.get('send_notifications', True),
        created_by=request.user
    )
    
    # Send notifications if enabled
    if meeting.send_notifications:
        users = User.objects.filter(is_active=True)
        notifications = []
        
        for user in users:
            notifications.append(Notification(
                user=user,
                title='New Meeting Scheduled',
                message=f'Meeting "{meeting.title}" has been scheduled.',
                notification_type='general'
            ))
        
        Notification.objects.bulk_create(notifications)
    
    return Response({
        'id': meeting.id,
        'message': 'Meeting created successfully'
    }, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdminOrStaff])
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

@api_view(['GET'])
@permission_classes([IsAdminOrStaff])
def admin_claims_list(request):
    """Get all claims for admin"""
    claims = Claim.objects.all().order_by('-created_at')
    claims_data = []
    
    for claim in claims:
        claims_data.append({
            'id': claim.id,
            'user': claim.user.username if claim.user else 'Unknown',
            'user_email': claim.user.email if claim.user else '',
            'claim_type': claim.get_claim_type_display(),
            'amount_requested': str(claim.amount_requested),
            'amount_approved': str(claim.amount_approved) if claim.amount_approved else None,
            'status': claim.status,
            'status_display': claim.get_status_display(),
            'description': claim.description,
            'supporting_documents': claim.supporting_documents.url if claim.supporting_documents else None,
            'admin_notes': claim.admin_notes,
            'created_at': claim.created_at.isoformat(),
            'updated_at': claim.updated_at.isoformat()
        })
    
    return Response(claims_data)

@api_view(['PATCH'])
@permission_classes([IsAdminOrStaff])
def admin_update_claim_status(request, claim_id):
    """Update claim status (admin only)"""
    from django.utils import timezone
    try:
        claim = Claim.objects.get(id=claim_id)
        
        if 'status' in request.data:
            claim.status = request.data['status']
        if 'amount_approved' in request.data:
            claim.amount_approved = request.data['amount_approved']
        if 'admin_notes' in request.data:
            claim.admin_notes = request.data['admin_notes']
        
        claim.reviewed_by = request.user
        claim.reviewed_at = timezone.now()
        claim.save()
        
        return Response({
            'id': claim.id,
            'status': claim.status,
            'message': 'Claim updated successfully'
        })
        
    except Claim.DoesNotExist:
        return Response({'error': 'Claim not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAdminOrStaff])
def make_user_admin(request, user_id):
    """Promote user to admin"""
    try:
        user = User.objects.get(id=user_id)
        user.is_staff = True
        user.save()
        
        return Response({
            'message': f'User {user.username} promoted to admin successfully'
        })
        
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAdminOrStaff])
def get_application_documents(request, app_id):
    """Get application documents"""
    try:
        application = Application.objects.get(id=app_id)
        documents = []
        
        # Check for document fields in application model
        if hasattr(application, 'documents_review_notes') and application.documents_review_notes:
            documents.append({
                'type': 'review_notes',
                'content': application.documents_review_notes
            })
        
        return Response({
            'application_id': app_id,
            'documents': documents,
            'applicant': f'{application.first_name} {application.last_name}'
        })
        
    except Application.DoesNotExist:
        return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAdminOrStaff])
def admin_payments_list(request):
    """Get all payments for admin"""
    payments = Payment.objects.all().order_by('-created_at')
    payments_data = []
    
    for payment in payments:
        payments_data.append({
            'id': payment.id,
            'user': payment.user.username if payment.user else 'Unknown',
            'user_email': payment.user.email if payment.user else '',
            'amount': str(payment.amount),
            'payment_method': payment.payment_method,
            'status': payment.status,
            'transaction_id': payment.transaction_id,
            'created_at': payment.created_at.isoformat(),
            'updated_at': payment.updated_at.isoformat()
        })
    
    return Response(payments_data)