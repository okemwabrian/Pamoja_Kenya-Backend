from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model

User = get_user_model()

class IsRegisteredMember(BasePermission):
    """
    Custom permission to only allow registered members to access the system.
    """
    
    def has_permission(self, request, view):
        # Allow unauthenticated access to login and register endpoints
        if request.path in ['/api/auth/login/', '/api/auth/register/']:
            return True
            
        # For other endpoints, user must be authenticated and active
        if not request.user or not request.user.is_authenticated:
            return False
            
        # Check if user is active and has valid membership
        return (
            request.user.is_active and 
            hasattr(request.user, 'membership_status') and
            request.user.membership_status in ['active', 'pending']
        )