from rest_framework import generics, status, parsers
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from django.utils import timezone
from .models import Claim, Beneficiary, BenefitPayment
from .serializers import ClaimSerializer, ClaimCreateSerializer, BeneficiarySerializer
from notifications.models import Notification

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([parsers.MultiPartParser, parsers.FormParser])
def submit_claim(request):
    """Submit claim with multipart form data and file upload"""
    # Get user
    user = request.user
    
    # Create claim with form data
    claim_data = {
        'claim_type': request.data.get('claim_type'),
        'amount_requested': request.data.get('amount_requested'),
        'description': request.data.get('description'),
        'supporting_documents': request.FILES.get('supporting_documents')
    }
    
    # Validate required fields
    required_fields = ['claim_type', 'amount_requested', 'description']
    for field in required_fields:
        if not claim_data.get(field):
            return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create claim
    claim = Claim.objects.create(
        user=user,
        claim_type=claim_data['claim_type'],
        amount_requested=claim_data['amount_requested'],
        description=claim_data['description'],
        supporting_documents=claim_data.get('supporting_documents')
    )
    
    # Create notification for user
    Notification.objects.create(
        user=user,
        title='Claim Submitted',
        message=f'Your {claim.get_claim_type_display()} claim for ${claim.amount_requested} has been submitted.',
        notification_type='claim_submitted'
    )
    
    return Response({
        'id': claim.id,
        'claim_type': claim.get_claim_type_display(),
        'amount_requested': str(claim.amount_requested),
        'status': claim.status,
        'message': 'Claim submitted successfully'
    }, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def create_claim(request):
    """Handle both listing and creating claims"""
    if request.method == 'GET':
        claims = Claim.objects.filter(user=request.user)
        serializer = ClaimSerializer(claims, many=True)
        return Response(serializer.data)
    
    # POST method
    serializer = ClaimCreateSerializer(data=request.data)
    if serializer.is_valid():
        claim = serializer.save(user=request.user)
        
        # Create notification for user
        Notification.objects.create(
            user=request.user,
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def claim_documents(request, claim_id):
    """Get documents for specific claim"""
    try:
        claim = Claim.objects.get(id=claim_id)
        # Check if user owns the claim or is admin
        if claim.user != request.user and not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        documents = []
        if claim.supporting_documents:
            documents.append({
                'id': 1,
                'name': 'Supporting Document',
                'file_url': claim.supporting_documents.url,
                'uploaded_at': claim.created_at.isoformat()
            })
        
        return Response(documents)
    except Claim.DoesNotExist:
        return Response({'error': 'Claim not found'}, status=status.HTTP_404_NOT_FOUND)