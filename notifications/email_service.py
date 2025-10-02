from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import Notification, ContactMessage, AdminNotification

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

def send_welcome_email(user):
    """Send welcome email after user registration"""
    subject = 'Welcome to Pamoja Kenya MN - Your Account is Ready!'
    
    context = {
        'user': user,
        'site_name': 'Pamoja Kenya MN',
        'frontend_url': settings.FRONTEND_URL
    }
    
    html_message = render_to_string('emails/welcome_email.html', context)
    plain_message = f"""
    Dear {user.first_name} {user.last_name},
    
    Welcome to Pamoja Kenya MN!
    
    Your account has been successfully created. You can now:
    - Submit membership applications
    - Make payments
    - Track your application status
    - Receive important updates
    
    Login to your account: {settings.FRONTEND_URL}/login
    
    If you have any questions, please contact our support team.
    
    Best regards,
    Pamoja Kenya MN Team
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        # Create notification
        Notification.objects.create(
            user=user,
            title='Welcome to Pamoja Kenya!',
            message='Your account has been created successfully. Welcome to our community!',
            notification_type='general'
        )
        
        return True
    except Exception as e:
        print(f"Failed to send welcome email: {e}")
        return False

def send_application_confirmation_email(user, application):
    """Send confirmation email after application submission"""
    subject = 'Application Submitted - Pamoja Kenya MN'
    
    context = {
        'user': user,
        'application': application,
        'site_name': 'Pamoja Kenya MN',
        'frontend_url': settings.FRONTEND_URL
    }
    
    html_message = render_to_string('emails/application_confirmation.html', context)
    plain_message = f"""
    Dear {application.full_name},
    
    Thank you for submitting your membership application to Pamoja Kenya MN!
    
    Application Details:
    - Application Type: {application.application_type.title()} Family
    - Full Name: {application.full_name}
    - Email: {application.email}
    - Phone: {application.phone}
    - Amount: ${application.amount}
    - Status: Under Review
    
    Your application is now under review. You will receive an email notification once the review is complete.
    
    You can track your application status by logging into your account: {settings.FRONTEND_URL}/dashboard
    
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
            title='Application Submitted',
            message=f'Your {application.application_type} family application has been submitted and is under review.',
            notification_type='application_submitted'
        )
        
        return True
    except Exception as e:
        print(f"Failed to send application confirmation email: {e}")
        return False

def send_claim_status_email(user, claim):
    """Send email when claim status is updated"""
    status_text = claim.get_status_display()
    subject = f'Claim {status_text} - Pamoja Kenya MN'
    
    context = {
        'user': user,
        'claim': claim,
        'status_text': status_text,
        'site_name': 'Pamoja Kenya MN',
        'frontend_url': settings.FRONTEND_URL
    }
    
    html_message = render_to_string('emails/claim_status_update.html', context)
    
    if claim.status == 'approved':
        message_content = f"Your claim for {claim.beneficiary.full_name} has been approved. The claim amount of ${claim.amount} will be processed."
        notification_type = 'claim_approved'
    elif claim.status == 'rejected':
        message_content = f"Your claim for {claim.beneficiary.full_name} has been rejected. Please contact support for more information."
        notification_type = 'claim_rejected'
    else:
        message_content = f"Your claim status has been updated to {status_text}."
        notification_type = 'claim_submitted'
    
    plain_message = f"""
    Dear {user.first_name} {user.last_name},
    
    Your claim status has been updated.
    
    Claim Details:
    - Beneficiary: {claim.beneficiary.full_name}
    - Amount: ${claim.amount}
    - Status: {status_text}
    - Date: {claim.created_at.strftime('%B %d, %Y')}
    
    {message_content}
    
    {'Reason: ' + claim.admin_notes if claim.admin_notes else ''}
    
    You can view your claim details by logging into your account: {settings.FRONTEND_URL}/claims
    
    Best regards,
    Pamoja Kenya MN Team
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        # Create notification
        Notification.objects.create(
            user=user,
            title=f'Claim {status_text}',
            message=message_content,
            notification_type=notification_type
        )
        
        return True
    except Exception as e:
        print(f"Failed to send claim status email: {e}")
        return False

def send_contact_form_notification(contact_message):
    """Send notification to admin when contact form is submitted"""
    subject = f'New Contact Form Submission - {contact_message.subject}'
    
    admin_emails = ['admin@pamojakenyamn.com']  # Add actual admin emails
    
    plain_message = f"""
    New contact form submission received:
    
    Name: {contact_message.name}
    Email: {contact_message.email}
    Phone: {contact_message.phone}
    Subject: {contact_message.subject}
    Help Type: {contact_message.get_help_type_display()}
    
    Message:
    {contact_message.message}
    
    Submitted: {contact_message.created_at.strftime('%B %d, %Y at %I:%M %p')}
    
    Please respond to this inquiry promptly.
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=admin_emails,
            fail_silently=False,
        )
        
        # Create admin notification
        AdminNotification.objects.create(
            type='contact_form',
            title=f'New Contact: {contact_message.subject}',
            message=f'New contact form from {contact_message.name} ({contact_message.email})',
            priority='medium',
            contact_message=contact_message
        )
        
        return True
    except Exception as e:
        print(f"Failed to send contact form notification: {e}")
        return False

def send_password_reset_email(user, reset_url):
    """Send password reset email"""
    subject = 'Password Reset Request - Pamoja Kenya MN'
    
    context = {
        'user': user,
        'reset_url': reset_url,
        'site_name': 'Pamoja Kenya MN',
        'frontend_url': settings.FRONTEND_URL
    }
    
    html_message = render_to_string('emails/password_reset.html', context)
    plain_message = f"""
    Dear {user.first_name} {user.last_name},
    
    You have requested to reset your password for your Pamoja Kenya MN account.
    
    Click the link below to reset your password:
    {reset_url}
    
    This link will expire in 24 hours for security reasons.
    
    If you did not request this password reset, please ignore this email.
    
    Best regards,
    Pamoja Kenya MN Team
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return True
    except Exception as e:
        print(f"Failed to send password reset email: {e}")
        return False

def generate_password_reset_url(user):
    """Generate password reset URL with token"""
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
    return reset_url