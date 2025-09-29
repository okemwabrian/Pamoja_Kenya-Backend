from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.utils import timezone
from .models import Application

@api_view(['POST'])
@permission_classes([AllowAny])
def create_application(request):
    """Create a new membership application"""
    data = request.data
    
    application = Application.objects.create(
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
        emergency_contact_name=data.get('emergency_contact_name', ''),
        emergency_contact_phone=data.get('emergency_contact_phone', ''),
        emergency_contact_relationship=data.get('emergency_contact_relationship', ''),
        constitution_agreed=data.get('constitution_agreed', False),
        amount=data.get('amount', 0),
        notes=data.get('notes', ''),
        status='pending'
    )
    
    return Response({
        'id': application.id,
        'message': 'Application submitted successfully',
        'status': application.status
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def my_applications(request):
    """Get applications for current user"""
    # Mock data for testing
    applications = [
        {
            'id': 1,
            'type': 'Single Family',
            'status': 'approved',
            'amount': 627.30,
            'created_at': '2025-09-20'
        },
        {
            'id': 2,
            'type': 'Double Family',
            'status': 'pending',
            'amount': 1254.60,
            'created_at': '2025-09-25'
        }
    ]
    
    return Response(applications)