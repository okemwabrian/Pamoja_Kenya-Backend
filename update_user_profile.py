from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User

@api_view(['POST'])
def update_profile(request):
    try:
        # In real app, get user from token
        # For now, use mock data
        data = request.data
        
        return Response({
            'message': 'Profile updated successfully',
            'user': {
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name'),
                'email': data.get('email'),
                'phone': data.get('phone'),
                'address': data.get('address'),
                'city': data.get('city'),
                'state': data.get('state'),
                'zip_code': data.get('zip_code')
            }
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def change_password(request):
    try:
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        
        if not current_password or not new_password:
            return Response({'error': 'Both current and new passwords are required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Mock password change
        return Response({'message': 'Password changed successfully'})
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)