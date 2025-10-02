from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum
from applications.models import Application
from claims.models import Claim
from payments.models import Payment

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Get user's dashboard statistics"""
    user = request.user
    
    # Get user's applications
    applications = Application.objects.filter(user=user)
    claims = Claim.objects.filter(user=user)
    payments = Payment.objects.filter(user=user)
    
    # Calculate stats
    total_paid = payments.aggregate(total=Sum('amount'))['total'] or 0
    last_payment = payments.order_by('-created_at').first()
    
    stats = {
        'membership_type': 'Single',  # Default
        'membership_status': getattr(user, 'membership_status', 'Active'),
        'total_applications': applications.count(),
        'pending_applications': applications.filter(status='pending').count(),
        'total_claims': claims.count(),
        'pending_claims': claims.filter(status='pending').count(),
        'total_paid': float(total_paid),
        'current_shares': 200,  # Default
        'last_payment_date': last_payment.created_at.strftime('%Y-%m-%d') if last_payment else None,
        'membership_start_date': user.date_joined.strftime('%Y-%m-%d')
    }
    
    return Response(stats)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_activities(request):
    """Get user's recent activities"""
    user = request.user
    activities = []
    
    # Recent applications
    applications = Application.objects.filter(user=user).order_by('-created_at')[:5]
    for app in applications:
        activities.append({
            'id': app.id,
            'type': 'application',
            'action': 'Application Submitted',
            'description': f'{app.application_type} Application submitted for ${app.amount}',
            'created_at': app.created_at.isoformat(),
            'status': app.status
        })
    
    # Recent claims
    claims = Claim.objects.filter(user=user).order_by('-created_at')[:5]
    for claim in claims:
        activities.append({
            'id': claim.id,
            'type': 'claim',
            'action': 'Claim Filed',
            'description': f'{claim.get_claim_type_display()} claim for ${claim.amount_requested} submitted',
            'created_at': claim.created_at.isoformat(),
            'status': claim.status
        })
    
    # Recent payments
    payments = Payment.objects.filter(user=user).order_by('-created_at')[:5]
    for payment in payments:
        activities.append({
            'id': payment.id,
            'type': 'payment',
            'action': 'Payment Made',
            'description': f'Payment of ${payment.amount} processed successfully',
            'created_at': payment.created_at.isoformat(),
            'status': payment.status
        })
    
    # Sort by date
    activities.sort(key=lambda x: x['created_at'], reverse=True)
    
    return Response(activities[:10])