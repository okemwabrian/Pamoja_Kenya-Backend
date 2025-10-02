from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.utils import timezone
from .models import Application
from notifications.email_service import send_application_confirmation_email

@api_view(['POST'])
@permission_classes([AllowAny])
def create_application(request):
    """Create a new membership application"""
    data = request.data
    
    # Get user from token or use default for testing
    from accounts.models import User
    if request.user.is_authenticated:
        user = request.user
    else:
        user, created = User.objects.get_or_create(
            email='test@example.com',
            defaults={'username': 'testuser', 'first_name': 'Test', 'last_name': 'User'}
        )
    
    application = Application.objects.create(
        user=user,
        application_type=data.get('application_type', 'single'),
        first_name=data.get('first_name'),
        middle_name=data.get('middle_name', ''),
        last_name=data.get('last_name'),
        email=data.get('email'),
        phone=data.get('phone'),
        address=data.get('address'),
        city=data.get('city'),
        state=data.get('state'),
        zip_code=data.get('zip_code'),
        spouse_name=data.get('spouse_name', ''),
        spouse_phone=data.get('spouse_phone', ''),
        authorized_rep=data.get('authorized_rep', ''),
        child_1=data.get('child_1', ''),
        child_2=data.get('child_2', ''),
        child_3=data.get('child_3', ''),
        child_4=data.get('child_4', ''),
        child_5=data.get('child_5', ''),
        parent_1=data.get('parent_1', ''),
        parent_2=data.get('parent_2', ''),
        spouse_parent_1=data.get('spouse_parent_1', ''),
        spouse_parent_2=data.get('spouse_parent_2', ''),
        sibling_1=data.get('sibling_1', ''),
        sibling_2=data.get('sibling_2', ''),
        sibling_3=data.get('sibling_3', ''),
        emergency_contact_name=data.get('emergency_contact_name', ''),
        emergency_contact_phone=data.get('emergency_contact_phone', ''),
        emergency_contact_relationship=data.get('emergency_contact_relationship', ''),
        constitution_agreed=data.get('constitution_agreed', False),
        amount=data.get('amount', 0),
        notes=data.get('notes', ''),
        status='pending'
    )
    
    # Send application confirmation email
    send_application_confirmation_email(user, application)
    
    return Response({
        'id': application.id,
        'message': 'Application submitted successfully',
        'status': application.status
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def my_applications(request):
    """Get applications for current user"""
    if request.user.is_authenticated:
        applications = Application.objects.filter(user=request.user)
    else:
        # For testing, show recent applications
        applications = Application.objects.all().order_by('-created_at')[:5]
    
    applications_data = []
    for app in applications:
        applications_data.append({
            'id': app.id,
            'type': app.get_application_type_display(),
            'status': app.status,
            'amount': float(app.amount),
            'created_at': app.created_at.strftime('%Y-%m-%d'),
            'first_name': app.first_name,
            'last_name': app.last_name,
            'email': app.email
        })
    
    return Response(applications_data)

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_application(request):
    """Submit new application"""
    data = request.data
    
    # Get user from token or use default for testing
    from accounts.models import User
    if request.user.is_authenticated:
        user = request.user
    else:
        user, created = User.objects.get_or_create(
            email='test@example.com',
            defaults={'username': 'testuser', 'first_name': 'Test', 'last_name': 'User'}
        )
    
    # Set amount based on application type
    app_type = data.get('application_type', 'single')
    amount = 200 if app_type == 'single' else 400
    
    application = Application.objects.create(
        user=user,
        application_type=app_type,
        first_name=data.get('first_name'),
        middle_name=data.get('middle_name', ''),
        last_name=data.get('last_name'),
        email=data.get('email'),
        phone=data.get('phone'),
        address=data.get('address'),
        city=data.get('city'),
        state=data.get('state'),
        zip_code=data.get('zip_code'),
        amount=amount,
        registration_fee=data.get('registration_fee', 50.00),
        constitution_agreed=data.get('constitution_agreed', False),
        status='pending'
    )
    
    # Send application confirmation email
    send_application_confirmation_email(user, application)
    
    return Response({
        'id': application.id,
        'message': 'Application submitted successfully',
        'status': application.status,
        'amount': float(application.amount)
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def application_documents(request, application_id):
    """Get documents for specific application"""
    try:
        application = Application.objects.get(id=application_id)
        # Mock document data
        documents = [
            {
                'id': 1,
                'name': 'ID Document',
                'file_url': '/media/documents/id_doc.pdf',
                'uploaded_at': '2025-09-28T10:00:00Z'
            }
        ]
        return Response(documents)
    except Application.DoesNotExist:
        return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)