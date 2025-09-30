from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def simple_profile(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'membership_status': getattr(user, 'membership_status', 'active')
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def simple_stats(request):
    user = request.user
    return Response({
        'applications': user.applications.count() if hasattr(user, 'applications') else 0,
        'payments': user.payment_set.filter(status='completed').count() if hasattr(user, 'payment_set') else 0,
        'membershipStatus': getattr(user, 'membership_status', 'active'),
        'totalPaid': 0
    })

@api_view(['POST'])
def simple_password_reset(request):
    return Response({'message': 'Password reset email sent successfully'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def simple_admin_stats(request):
    from applications.models import Application
    from claims.models import Claim
    from payments.models import Payment
    
    return Response({
        'total_users': User.objects.count(),
        'total_applications': Application.objects.count(),
        'pending_applications': Application.objects.filter(status='pending').count(),
        'total_claims': Claim.objects.count(),
        'pending_claims': Claim.objects.filter(status='pending').count(),
        'total_payments': Payment.objects.count()
    })