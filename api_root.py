from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """API root endpoint"""
    return Response({
        'message': 'Pamoja Kenya API',
        'version': '1.0',
        'endpoints': {
            'auth': '/api/auth/',
            'applications': '/api/applications/',
            'payments': '/api/payments/',
            'beneficiaries': '/api/beneficiaries/',
            'claims': '/api/claims/',
            'notifications': '/api/notifications/',
            'admin': '/api/admin/'
        }
    })