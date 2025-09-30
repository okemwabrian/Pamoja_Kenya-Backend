from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Notification
from .firebase_email_service import firebase_email_service

def send_registration_email(user, application):
    """Send email when user registers"""
    # Use Firebase email service if configured
    if getattr(settings, 'USE_FIREBASE_EMAIL', False):
        return firebase_email_service.send_application_confirmation(user, application)
    
    # Fallback to Django email
    subject = 'Welcome to Pamoja Kenya - Registration Received'
    
    context = {
        'user': user,
        'application': application,
        'site_name': 'Pamoja Kenya MN'
    }
    
    html_message = render_to_string('emails/registration_confirmation.html', context)
    plain_message = f"""
    Dear {application.full_name},
    
    Thank you for registering with Pamoja Kenya MN!
    
    Your {application.application_type} family application has been received and is currently under review.
    
    Application Details:
    - Name: {application.full_name}
    - Email: {application.email}
    - Phone: {application.phone}
    - Amount: ${application.amount}
    
    You will receive an email notification once your application has been reviewed.
    
    Best regards,
    Pamoja Kenya MN Team
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[application.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        # Create notification
        Notification.objects.create(
            user=user,
            title='Registration Confirmation',
            message=f'Your {application.application_type} family application has been submitted successfully.',
            notification_type='application_submitted'
        )
        
        return True
    except Exception as e:
        print(f"Failed to send registration email: {e}")
        return False

def send_approval_email(user, application):
    """Send email when application is approved"""
    # Use Firebase email service if configured
    if getattr(settings, 'USE_FIREBASE_EMAIL', False):
        return firebase_email_service.send_application_status_update(user, application)
    
    # Fallback to Django email
    subject = 'Congratulations! Your Pamoja Kenya Application Approved'
    
    context = {
        'user': user,
        'application': application,
        'site_name': 'Pamoja Kenya MN'
    }
    
    html_message = render_to_string('emails/application_approved.html', context)
    plain_message = f"""
    Dear {application.full_name},
    
    Congratulations! Your {application.application_type} family application has been APPROVED!
    
    You are now a member of Pamoja Kenya MN. Welcome to our community!
    
    Next Steps:
    1. Complete your payment if not already done
    2. Log in to your dashboard to view your membership details
    3. Stay updated with upcoming events and announcements
    
    Best regards,
    Pamoja Kenya MN Team
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[application.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        # Create notification
        Notification.objects.create(
            user=user,
            title='Application Approved!',
            message=f'Congratulations! Your {application.application_type} family application has been approved.',
            notification_type='application_approved'
        )
        
        return True
    except Exception as e:
        print(f"Failed to send approval email: {e}")
        return False

def send_rejection_email(user, application, reason):
    """Send email when application is rejected"""
    subject = 'Pamoja Kenya Application Update Required'
    
    context = {
        'user': user,
        'application': application,
        'reason': reason,
        'site_name': 'Pamoja Kenya MN'
    }
    
    html_message = render_to_string('emails/application_rejected.html', context)
    plain_message = f"""
    Dear {application.full_name},
    
    Thank you for your interest in Pamoja Kenya MN.
    
    We have reviewed your {application.application_type} family application and need some additional information or corrections.
    
    Reason for review request:
    {reason}
    
    Please log in to your account to make the necessary updates and resubmit your application.
    
    If you have any questions, please contact our support team.
    
    Best regards,
    Pamoja Kenya MN Team
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[application.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        # Create notification
        Notification.objects.create(
            user=user,
            title='Application Needs Updates',
            message=f'Your {application.application_type} family application requires updates. Please check your email for details.',
            notification_type='application_rejected'
        )
        
        return True
    except Exception as e:
        print(f"Failed to send rejection email: {e}")
        return False

def send_document_review_email(user, application):
    """Send document review notification email"""
    # Use Firebase email service if configured
    if getattr(settings, 'USE_FIREBASE_EMAIL', False):
        return firebase_email_service.send_document_review_notification(user, application)
    
    # Fallback to Django email
    status_text = application.get_identity_document_status_display()
    subject = f'Document Review {status_text} - Pamoja Kenya MN'
    
    message = f"""
    Dear {user.first_name} {user.last_name},
    
    We have completed the review of your submitted documents for Application #{application.id}.
    
    Document Status: {status_text}
    
    {'Your documents have been approved and your application will proceed to the next stage.' if application.identity_document_status == 'approved' else 'Your documents require resubmission. Please check your account for details and resubmit corrected documents.'}
    
    {f'Review Notes: {application.documents_review_notes}' if application.documents_review_notes else ''}
    
    Best regards,
    Pamoja Kenya MN Team
    """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        # Create notification
        Notification.objects.create(
            user=user,
            title=f'Documents {status_text}',
            message=f'Your submitted documents have been {status_text.lower()}.',
            notification_type='application_submitted'
        )
        
        return True
    except Exception as e:
        print(f"Error sending document review email: {e}")
        return False

def send_payment_confirmation_email(user, payment):
    """Send email when payment is received"""
    # Use Firebase email service if configured
    if getattr(settings, 'USE_FIREBASE_EMAIL', False):
        return firebase_email_service.send_payment_confirmation(user, payment)
    
    # Fallback to Django email
    subject = 'Payment Confirmation - Pamoja Kenya MN'
    
    context = {
        'user': user,
        'payment': payment,
        'site_name': 'Pamoja Kenya MN'
    }
    
    html_message = render_to_string('emails/payment_confirmation.html', context)
    plain_message = f"""
    Dear {payment.payer_name},
    
    Thank you for your payment to Pamoja Kenya MN!
    
    Payment Details:
    - Amount: ${payment.amount}
    - Payment Method: {payment.payment_method.title()}
    - Transaction ID: {payment.transaction_id or payment.paypal_order_id or payment.stripe_payment_intent_id}
    - Date: {payment.created_at.strftime('%B %d, %Y')}
    
    Your payment has been successfully processed and your membership is now active.
    
    Best regards,
    Pamoja Kenya MN Team
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[payment.payer_email],
            html_message=html_message,
            fail_silently=False,
        )
        
        # Create notification
        Notification.objects.create(
            user=user,
            title='Payment Received',
            message=f'Your payment of ${payment.amount} has been successfully processed.',
            notification_type='payment_received'
        )
        
        return True
    except Exception as e:
        print(f"Failed to send payment confirmation email: {e}")
        return False