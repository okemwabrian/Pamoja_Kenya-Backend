from celery import shared_task
from email_service import EmailService
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_welcome_email_task(user_email, user_name):
    """Async task to send welcome email"""
    try:
        result = EmailService.send_welcome_email(user_email, user_name)
        logger.info(f"Welcome email task completed for {user_email}: {result}")
        return result
    except Exception as e:
        logger.error(f"Welcome email task failed for {user_email}: {str(e)}")
        return False

@shared_task
def send_payment_confirmation_task(user_email, user_name, payment_details):
    """Async task to send payment confirmation email"""
    try:
        result = EmailService.send_payment_confirmation(user_email, user_name, payment_details)
        logger.info(f"Payment confirmation email task completed for {user_email}: {result}")
        return result
    except Exception as e:
        logger.error(f"Payment confirmation email task failed for {user_email}: {str(e)}")
        return False

@shared_task
def send_application_status_task(user_email, user_name, status, application_type):
    """Async task to send application status email"""
    try:
        result = EmailService.send_application_status_email(user_email, user_name, status, application_type)
        logger.info(f"Application status email task completed for {user_email}: {result}")
        return result
    except Exception as e:
        logger.error(f"Application status email task failed for {user_email}: {str(e)}")
        return False