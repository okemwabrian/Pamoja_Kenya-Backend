from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([AllowAny])
def test_simple_app(request):
    """Simple test endpoint"""
    return Response({'message': 'Test successful'}, status=status.HTTP_200_OK)