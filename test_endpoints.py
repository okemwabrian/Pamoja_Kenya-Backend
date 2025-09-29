from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def test_endpoint(request):
    if request.method == 'GET':
        return Response({'message': 'Test endpoint working!', 'method': 'GET'})
    elif request.method == 'POST':
        return Response({
            'message': 'Test POST working!', 
            'data': request.data,
            'method': 'POST'
        }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def simple_claim_submit(request):
    return Response({
        'message': 'Claim submitted successfully!',
        'id': 1,
        'data': request.data
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def simple_claims_list(request):
    return Response([
        {
            'id': 1,
            'claim_type': 'Death Benefit',
            'amount_requested': '5000.00',
            'status': 'Pending',
            'description': 'Test claim',
            'created_at': '2025-09-28'
        }
    ])