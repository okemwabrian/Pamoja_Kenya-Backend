from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from email_service import EmailService
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def contact_form(request):
    """Handle contact form submissions"""
    try:
        data = request.data
        
        # Get form data
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        subject = data.get('subject', '').strip()
        help_type = data.get('help_type', 'membership')
        message = data.get('message', '').strip()
        
        # Validation
        if not all([name, email, subject, message]):
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Send email notification
        try:
            EmailService.send_contact_email(name, email, subject, message, help_type)
        except Exception as e:
            logger.error(f"Failed to send contact email: {str(e)}")
        
        return Response({
            'message': 'Contact form submitted successfully',
            'status': 'success'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Contact form error: {str(e)}")
        return Response({'error': 'Failed to submit contact form'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)