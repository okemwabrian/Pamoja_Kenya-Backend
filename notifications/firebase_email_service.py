import json
import requests
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)

class FirebaseEmailService:
    """
    Firebase Email Service for sending emails through Firebase Functions
    """
    
    def __init__(self):
        self.firebase_function_url = getattr(settings, 'FIREBASE_EMAIL_FUNCTION_URL', None)
        self.firebase_api_key = getattr(settings, 'FIREBASE_API_KEY', None)
        
    def send_email(self, to_email, subject, html_content, text_content=None):
        """
        Send email through Firebase Function
        """
        if not self.firebase_function_url:
            logger.warning("Firebase email function URL not configured")
            return False
            
        if not text_content:
            text_content = strip_tags(html_content)
            
        payload = {
            'to': to_email,
            'subject': subject,
            'html': html_content,
            'text': text_content
        }
        
        headers = {
            'Content-Type': 'application/json',
        }
        
        if self.firebase_api_key:
            headers['Authorization'] = f'Bearer {self.firebase_api_key}'
            
        try:
            response = requests.post(
                self.firebase_function_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Failed to send email to {to_email}: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending email to {to_email}: {str(e)}")
            return False
    
    def send_application_confirmation(self, user, application):
        """
        Send application confirmation email
        """
        subject = "Application Received - Pamoja Kenya MN"
        
        context = {
            'user': user,
            'application': application,
            'site_name': 'Pamoja Kenya MN'
        }
        
        html_content = render_to_string('emails/application_confirmation.html', context)
        text_content = render_to_string('emails/application_confirmation.txt', context)
        
        return self.send_email(user.email, subject, html_content, text_content)
    
    def send_application_status_update(self, user, application):
        """
        Send application status update email
        """
        status_text = application.get_status_display()
        subject = f"Application {status_text} - Pamoja Kenya MN"
        
        context = {
            'user': user,
            'application': application,
            'status_text': status_text,
            'site_name': 'Pamoja Kenya MN'
        }
        
        html_content = render_to_string('emails/application_status_update.html', context)
        text_content = render_to_string('emails/application_status_update.txt', context)
        
        return self.send_email(user.email, subject, html_content, text_content)
    
    def send_document_review_notification(self, user, application):
        """
        Send document review notification email
        """
        status_text = application.get_identity_document_status_display()
        subject = f"Document Review {status_text} - Pamoja Kenya MN"
        
        context = {
            'user': user,
            'application': application,
            'document_status': status_text,
            'review_notes': application.documents_review_notes,
            'site_name': 'Pamoja Kenya MN'
        }
        
        html_content = render_to_string('emails/document_review_notification.html', context)
        text_content = render_to_string('emails/document_review_notification.txt', context)
        
        return self.send_email(user.email, subject, html_content, text_content)
    
    def send_payment_confirmation(self, user, payment):
        """
        Send payment confirmation email
        """
        subject = "Payment Received - Pamoja Kenya MN"
        
        context = {
            'user': user,
            'payment': payment,
            'site_name': 'Pamoja Kenya MN'
        }
        
        html_content = render_to_string('emails/payment_confirmation.html', context)
        text_content = render_to_string('emails/payment_confirmation.txt', context)
        
        return self.send_email(user.email, subject, html_content, text_content)
    
    def send_claim_notification(self, user, claim):
        """
        Send claim status notification email
        """
        status_text = claim.get_status_display()
        subject = f"Claim {status_text} - Pamoja Kenya MN"
        
        context = {
            'user': user,
            'claim': claim,
            'status_text': status_text,
            'site_name': 'Pamoja Kenya MN'
        }
        
        html_content = render_to_string('emails/claim_notification.html', context)
        text_content = render_to_string('emails/claim_notification.txt', context)
        
        return self.send_email(user.email, subject, html_content, text_content)

# Global instance
firebase_email_service = FirebaseEmailService()