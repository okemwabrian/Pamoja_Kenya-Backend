from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User

@api_view(['POST'])
def simple_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    try:
        user = User.objects.get(username=username)
        
        # Simple password check (not secure, just for testing)
        if user.check_password(password):
            return Response({
                'access': 'fake-token-' + str(user.id),
                'refresh': 'fake-refresh-' + str(user.id),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser
                }
            })
        else:
            return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
            
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)