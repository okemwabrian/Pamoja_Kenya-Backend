from rest_framework.decorators import api_view, permission_classes
nfrom rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from accounts.models import User
from accounts.serializers import UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def simple_login(request):
    """Simple working login endpoint"""
    identifier = request.data.get('identifier') or request.data.get('email')
    password = request.data.get('password')
    
    if not identifier or not password:
        return Response({'error': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Authenticate user
    user = authenticate(username=identifier, password=password)
    
    if user and user.is_active:
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)