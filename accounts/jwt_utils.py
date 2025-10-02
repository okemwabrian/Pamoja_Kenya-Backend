from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta

def create_tokens_for_user(user):
    """Create JWT tokens with different expiration for admins vs users"""
    refresh = RefreshToken.for_user(user)
    
    # Check if user is admin
    is_admin = user.is_staff or user.is_superuser
    
    if is_admin:
        # Set longer expiration for admins (30 days)
        refresh.set_exp(lifetime=timedelta(days=30))
        refresh.access_token.set_exp(lifetime=timedelta(days=30))
    else:
        # Regular users get 10 minutes (default is already set in settings)
        refresh.set_exp(lifetime=timedelta(days=1))
        refresh.access_token.set_exp(lifetime=timedelta(minutes=10))
    
    return refresh

class CustomRefreshToken(RefreshToken):
    """Wrapper for custom token creation"""
    
    @classmethod
    def for_user(cls, user):
        return create_tokens_for_user(user)