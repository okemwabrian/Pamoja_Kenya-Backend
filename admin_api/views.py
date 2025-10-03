from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from applications.models import Application
from claims.models import Claim
from notifications.models import Event, Announcement, Notification, Meeting, ContactMessage, AdminNotification
from payments.models import Payment
from .permissions import IsAdminOrStaff
from notifications.email_service import send_approval_email, send_rejection_email, send_claim_status_email

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAdminOrStaff])
def admin_dashboard_stats(request):
    """Get admin dashboard statistics"""
    stats = {
        'total_users': User.objects.count(),
        'total_applications': Application.objects.count(),
        'pending_applications': Application.objects.filter(status='pending').count(),
        'total_claims': Claim.objects.count(),
        'pending_claims': Claim.objects.filter(status='pending').count()
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
            'date_joined': user.date_joined.isoformat()
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
            'amount': float(app.amount),
            'status': app.status,
            'created_at': app.created_at.isoformat()
        })
    
    return Response(apps_data)

@api_view(['POST'])
@permission_classes([IsAdminOrStaff])
def update_application_status(request, app_id):
    """Update application status"""
    try:
        application = Application.objects.get(id=app_id)
        new_status = request.data.get('status')
        reason = request.data.get('reason', '')
        send_email = request.data.get('send_email', True)
        
        if new_status in ['approved', 'rejected']:
            application.status = new_status
            if hasattr(application, 'admin_notes'):
                application.admin_notes = reason
            application.save()
            
            # Send email notification if requested
            if send_email and hasattr(application, 'user') and application.user:
                if new_status == 'approved':
                    send_approval_email(application.user, application)
                elif new_status == 'rejected':
                    send_rejection_email(application.user, application, reason)
                
                # Create notification for user
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
        'title': announcement.title,
        'content': announcement.content,
        'priority': announcement.priority,
        'is_pinned': announcement.is_pinned,
        'created_by': announcement.created_by.username,
        'created_at': announcement.created_at.isoformat()
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
        'title': event.title,
        'description': event.description,
        'date': event.date.isoformat(),
        'location': event.location,
        'is_featured': event.is_featured,
        'registration_required': event.registration_required,
        'created_by': event.created_by.username,
        'created_at': event.created_at.isoformat()
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
        'title': meeting.title,
        'description': meeting.description,
        'date': meeting.date.isoformat(),
        'duration': meeting.duration,
        'type': meeting.type,
        'max_participants': meeting.max_participants,
        'meeting_link': meeting.meeting_link,
        'require_registration': meeting.require_registration,
        'created_by': meeting.created_by.username,
        'created_at': meeting.created_at.isoformat()
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
        claim_data = {
            'id': claim.id,
            'user': {'username': claim.user.username if claim.user else 'Unknown'},
            'claim_type': claim.get_claim_type_display(),
            'amount_requested': float(claim.amount_requested),
            'amount_approved': float(claim.amount_approved) if claim.amount_approved else 0,
            'status': claim.status,
            'description': claim.description,
            'admin_notes': claim.admin_notes or '',
            'supporting_documents': claim.supporting_documents.url if claim.supporting_documents else '',
            'created_at': claim.created_at.isoformat()
        }
            
        claims_data.append(claim_data)
    
    return Response(claims_data)

@api_view(['PATCH'])
@permission_classes([IsAdminOrStaff])
def admin_update_claim_status(request, claim_id):
    """Update claim status (admin only)"""
    from django.utils import timezone
    try:
        claim = Claim.objects.get(id=claim_id)
        
        new_status = request.data.get('status')
        admin_notes = request.data.get('admin_notes', '')
        amount_approved = request.data.get('amount_approved')
        send_email = request.data.get('send_email', True)
        
        if new_status in ['approved', 'rejected']:
            claim.status = new_status
            claim.admin_notes = admin_notes
            
            if amount_approved and new_status == 'approved':
                claim.amount_approved = amount_approved
            
            claim.reviewed_by = request.user
            claim.reviewed_at = timezone.now()
            claim.save()
            
            # Send email notification if requested
            if send_email and claim.user:
                send_claim_status_email(claim.user, claim)
            
            return Response({
                'id': claim.id,
                'status': claim.status,
                'message': 'Claim updated successfully'
            })
        else:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
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
        if hasattr(application, 'identity_document') and application.identity_document:
            documents.append({
                'id': 1,
                'name': 'Identity Document',
                'type': 'identity',
                'url': application.identity_document.url
            })
        
        if hasattr(application, 'supporting_document_1') and application.supporting_document_1:
            documents.append({
                'id': 2,
                'name': 'Supporting Document 1',
                'type': 'supporting',
                'url': application.supporting_document_1.url
            })
        
        return Response(documents)
        
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

# Content Management CRUD Operations
@api_view(['GET'])
@permission_classes([IsAdminOrStaff])
def admin_announcements_list(request):
    """Get all announcements for admin"""
    announcements = Announcement.objects.all().order_by('-created_at')
    data = []
    for ann in announcements:
        data.append({
            'id': ann.id,
            'title': ann.title,
            'content': ann.content,
            'priority': ann.priority,
            'is_pinned': ann.is_pinned,
            'is_active': ann.is_active,
            'created_by': ann.created_by.username,
            'created_at': ann.created_at.isoformat(),
            'updated_at': ann.updated_at.isoformat()
        })
    return Response(data)

@api_view(['PUT'])
@permission_classes([IsAdminOrStaff])
def admin_update_announcement(request, announcement_id):
    """Update announcement"""
    try:
        announcement = Announcement.objects.get(id=announcement_id)
        data = request.data
        
        announcement.title = data.get('title', announcement.title)
        announcement.content = data.get('content', announcement.content)
        announcement.priority = data.get('priority', announcement.priority)
        announcement.is_pinned = data.get('is_pinned', announcement.is_pinned)
        announcement.is_active = data.get('is_active', announcement.is_active)
        announcement.save()
        
        return Response({
            'id': announcement.id,
            'title': announcement.title,
            'content': announcement.content,
            'priority': announcement.priority,
            'is_pinned': announcement.is_pinned,
            'created_by': announcement.created_by.username,
            'created_at': announcement.created_at.isoformat()
        })
    except Announcement.DoesNotExist:
        return Response({'error': 'Announcement not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAdminOrStaff])
def admin_delete_announcement(request, announcement_id):
    """Delete announcement"""
    try:
        announcement = Announcement.objects.get(id=announcement_id)
        announcement.delete()
        return Response({'message': 'Announcement deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Announcement.DoesNotExist:
        return Response({'error': 'Announcement not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAdminOrStaff])
def admin_events_list(request):
    """Get all events for admin"""
    events = Event.objects.all().order_by('-created_at')
    data = []
    for event in events:
        data.append({
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'date': event.date.isoformat(),
            'location': event.location,
            'is_featured': event.is_featured,
            'registration_required': event.registration_required,
            'is_active': event.is_active,
            'created_by': event.created_by.username,
            'created_at': event.created_at.isoformat()
        })
    return Response(data)

@api_view(['PUT'])
@permission_classes([IsAdminOrStaff])
def admin_update_event(request, event_id):
    """Update event"""
    try:
        event = Event.objects.get(id=event_id)
        data = request.data
        
        event.title = data.get('title', event.title)
        event.description = data.get('description', event.description)
        if 'date' in data:
            event.date = data['date']
        event.location = data.get('location', event.location)
        event.is_featured = data.get('is_featured', event.is_featured)
        event.registration_required = data.get('registration_required', event.registration_required)
        event.is_active = data.get('is_active', event.is_active)
        event.save()
        
        return Response({
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'date': event.date.isoformat(),
            'location': event.location,
            'is_featured': event.is_featured,
            'registration_required': event.registration_required,
            'created_by': event.created_by.username,
            'created_at': event.created_at.isoformat()
        })
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAdminOrStaff])
def admin_delete_event(request, event_id):
    """Delete event"""
    try:
        event = Event.objects.get(id=event_id)
        event.delete()
        return Response({'message': 'Event deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAdminOrStaff])
def admin_meetings_list(request):
    """Get all meetings for admin"""
    meetings = Meeting.objects.all().order_by('-created_at')
    data = []
    for meeting in meetings:
        data.append({
            'id': meeting.id,
            'title': meeting.title,
            'description': meeting.description,
            'date': meeting.date.isoformat(),
            'duration': meeting.duration,
            'type': meeting.type,
            'max_participants': meeting.max_participants,
            'meeting_link': meeting.meeting_link,
            'require_registration': meeting.require_registration,
            'created_by': meeting.created_by.username,
            'created_at': meeting.created_at.isoformat()
        })
    return Response(data)

@api_view(['PUT'])
@permission_classes([IsAdminOrStaff])
def admin_update_meeting(request, meeting_id):
    """Update meeting"""
    try:
        meeting = Meeting.objects.get(id=meeting_id)
        data = request.data
        
        meeting.title = data.get('title', meeting.title)
        meeting.description = data.get('description', meeting.description)
        if 'date' in data:
            meeting.date = data['date']
        meeting.duration = data.get('duration', meeting.duration)
        meeting.type = data.get('type', meeting.type)
        meeting.max_participants = data.get('max_participants', meeting.max_participants)
        meeting.meeting_link = data.get('meeting_link', meeting.meeting_link)
        meeting.require_registration = data.get('require_registration', meeting.require_registration)
        meeting.save()
        
        return Response({
            'id': meeting.id,
            'title': meeting.title,
            'description': meeting.description,
            'date': meeting.date.isoformat(),
            'duration': meeting.duration,
            'type': meeting.type,
            'created_by': meeting.created_by.username,
            'created_at': meeting.created_at.isoformat()
        })
    except Meeting.DoesNotExist:
        return Response({'error': 'Meeting not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAdminOrStaff])
def admin_delete_meeting(request, meeting_id):
    """Delete meeting"""
    try:
        meeting = Meeting.objects.get(id=meeting_id)
        meeting.delete()
        return Response({'message': 'Meeting deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Meeting.DoesNotExist:
        return Response({'error': 'Meeting not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAdminOrStaff])
def admin_contacts_list(request):
    """Get all contact messages for admin"""
    contacts = ContactMessage.objects.all().order_by('-created_at')
    data = []
    for contact in contacts:
        data.append({
            'id': contact.id,
            'name': contact.name,
            'email': contact.email,
            'phone': contact.phone,
            'subject': contact.subject,
            'message': contact.message,
            'status': contact.status,
            'created_at': contact.created_at.isoformat()
        })
    return Response(data)

@api_view(['PATCH'])
@permission_classes([IsAdminOrStaff])
def admin_update_contact(request, contact_id):
    """Update contact message status and notes"""
    from django.utils import timezone
    try:
        contact = ContactMessage.objects.get(id=contact_id)
        data = request.data
        
        if 'status' in data:
            contact.status = data['status']
            if data['status'] == 'resolved' and not contact.resolved_at:
                contact.resolved_at = timezone.now()
        
        if 'admin_notes' in data:
            contact.admin_notes = data['admin_notes']
        
        contact.save()
        
        return Response({
            'id': contact.id,
            'name': contact.name,
            'email': contact.email,
            'subject': contact.subject,
            'status': contact.status,
            'admin_notes': contact.admin_notes,
            'message': 'Contact message updated successfully'
        })
    except ContactMessage.DoesNotExist:
        return Response({'error': 'Contact message not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAdminOrStaff])
def get_claim_documents(request, claim_id):
    """Get claim documents"""
    try:
        claim = Claim.objects.get(id=claim_id)
        documents = []
        
        if claim.supporting_documents:
            documents.append({
                'id': 1,
                'name': 'Supporting Documents',
                'type': 'supporting',
                'url': claim.supporting_documents.url
            })
        
        return Response(documents)
        
    except Claim.DoesNotExist:
        return Response({'error': 'Claim not found'}, status=status.HTTP_404_NOT_FOUND)