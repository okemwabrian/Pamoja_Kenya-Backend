from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from django.utils import timezone
from .models import Claim, Beneficiary, BenefitPayment
from .serializers import ClaimSerializer, ClaimCreateSerializer, BeneficiarySerializer
from notifications.models import Notification

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_claim(request):
    serializer = ClaimCreateSerializer(data=request.data)
    if serializer.is_valid():
        # Get user or create a test user
        from accounts.models import User
        user = request.user if request.user.is_authenticated else User.objects.first()
        if not user:
            user = User.objects.create_user(username='testuser', email='test@example.com')
        
        claim = serializer.save(user=user)
        
        # Create notification for user
        Notification.objects.create(
            user=user,
            title='Claim Submitted',
            message=f'Your {claim.get_claim_type_display()} claim for ${claim.amount_requested} has been submitted.',
            notification_type='claim_submitted'
        )
        
        return Response({
            'id': claim.id,
            'message': 'Claim submitted successfully'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_claims(request):
    claims = Claim.objects.filter(user=request.user)
    serializer = ClaimSerializer(claims, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_claims_list(request):
    claims = Claim.objects.all()
    claims_data = []
    
    for claim in claims:
        claims_data.append({
            'id': claim.id,
            'user': claim.user.username,
            'user_email': claim.user.email,
            'claim_type': claim.get_claim_type_display(),
            'amount_requested': str(claim.amount_requested),
            'amount_approved': str(claim.amount_approved) if claim.amount_approved else None,
            'status': claim.status,
            'status_display': claim.get_status_display(),
            'description': claim.description,
            'created_at': claim.created_at.strftime('%Y-%m-%d %H:%M'),
            'admin_notes': claim.admin_notes
        })
    
    return Response(claims_data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_review_claim(request, claim_id):
    try:
        claim = Claim.objects.get(id=claim_id)
        action = request.data.get('action')  # 'approve' or 'reject'
        admin_notes = request.data.get('admin_notes', '')
        amount_approved = request.data.get('amount_approved')
        
        if action == 'approve':
            claim.status = 'approved'
            claim.amount_approved = amount_approved or claim.amount_requested
            notification_message = f'Your {claim.get_claim_type_display()} claim has been approved for ${claim.amount_approved}.'
            notification_type = 'claim_approved'
        elif action == 'reject':
            claim.status = 'rejected'
            notification_message = f'Your {claim.get_claim_type_display()} claim has been rejected. {admin_notes}'
            notification_type = 'claim_rejected'
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        
        claim.admin_notes = admin_notes
        claim.reviewed_by = request.user
        claim.reviewed_at = timezone.now()
        claim.save()
        
        # Create notification for user
        Notification.objects.create(
            user=claim.user,
            title=f'Claim {action.title()}d',
            message=notification_message,
            notification_type=notification_type
        )
        
        return Response({'message': f'Claim {action}d successfully'})
        
    except Claim.DoesNotExist:
        return Response({'error': 'Claim not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def beneficiaries_list(request):
    beneficiaries = Beneficiary.objects.filter(is_active=True)
    beneficiaries_data = []
    
    for beneficiary in beneficiaries:
        beneficiaries_data.append({
            'id': beneficiary.id,
            'name': beneficiary.name,
            'user': beneficiary.user.username,
            'relationship': beneficiary.relationship,
            'total_benefits': str(beneficiary.total_benefits_received),
            'last_benefit_date': beneficiary.last_benefit_date.strftime('%Y-%m-%d') if beneficiary.last_benefit_date else None,
            'phone': beneficiary.phone,
            'email': beneficiary.email
        })
    
    return Response(beneficiaries_data)