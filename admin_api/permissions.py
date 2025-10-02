from rest_framework import permissions

class IsAdminOrStaff(permissions.BasePermission):
    """
    Custom permission to only allow admin users or staff users.
    """
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_staff or 
             request.user.is_superuser or 
             getattr(request.user, 'role', None) == 'admin')
        )