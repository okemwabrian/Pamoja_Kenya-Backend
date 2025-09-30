from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.db import models
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserSerializer,
    UserProfileSerializer
)

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    from django.contrib.auth import authenticate
    import logging
    logger = logging.getLogger(__name__)
    
    # Debug: Log incoming data
    logger.error(f"Login request data: {request.data}")
    
    # Get credentials from request - handle multiple field names
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    # Use identifier as fallback (some frontends send this)
    identifier = request.data.get('identifier') or username or email
    
    logger.error(f"Identifier: {identifier}, Password: {'***' if password else None}")
    
    if not identifier or not password:
        return Response({'error': 'Username/email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Try to authenticate
    user = None
    auth_email = None
    
    # If identifier looks like email, use it directly
    if '@' in identifier:
        auth_email = identifier
        logger.error(f"Using email directly: {auth_email}")
    else:
        # If it's a username, find the user and get their email
        try:
            user_obj = User.objects.get(username=identifier)
            auth_email = user_obj.email
            logger.error(f"Found user: {user_obj.username}, email: {auth_email}")
        except User.DoesNotExist:
            logger.error(f"User not found: {identifier}")
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Authenticate using email (since USERNAME_FIELD = 'email')
    if auth_email:
        logger.error(f"Authenticating with email: {auth_email}")
        user = authenticate(username=auth_email, password=password)
        logger.error(f"Authentication result: {user}")
    
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

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_view(request):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_profile_view(request):
    serializer = UserProfileSerializer(
        request.user, 
        data=request.data, 
        partial=request.method == 'PATCH'
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats_view(request):
    user = request.user
    stats = {
        'applications': user.applications.count() if hasattr(user, 'applications') else 0,
        'payments': user.payment_set.filter(status='completed').count() if hasattr(user, 'payment_set') else 0,
        'membershipStatus': getattr(user, 'membership_status', 'active'),
        'totalPaid': 0
    }
    return Response(stats)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def password_reset_request(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        # In production, send actual reset email
        return Response({'message': 'Password reset email sent successfully'})
    except User.DoesNotExist:
        return Response({'message': 'If the email exists, a reset link has been sent'})

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def contact_form(request):
    data = request.data
    required_fields = ['name', 'email', 'subject', 'message']
    
    if not all(data.get(field) for field in required_fields):
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'message': 'Contact form submitted successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def simple_login(request):
    """Simple working login endpoint"""
    from django.contrib.auth import authenticate
    
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

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def activities_view(request):
    """Get user activities/notifications"""
    return Response([])

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def notifications_list(request):
    """Get notifications list"""
    return Response([])

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def notifications_events(request):
    """Get notification events"""
    return Response([])

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def notifications_announcements(request):
    """Get notification announcements"""
    return Response([])

