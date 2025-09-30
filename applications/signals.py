from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Application
from notifications.email_service import send_registration_email, send_approval_email, send_rejection_email, send_document_review_email

@receiver(post_save, sender=Application)
def handle_application_created(sender, instance, created, **kwargs):
    """Send email when application is created"""
    if created:
        # Temporarily disabled for debugging
        pass

@receiver(pre_save, sender=Application)
def handle_application_status_change(sender, instance, **kwargs):
    """Send email when application status changes"""
    if instance.pk:  # Only for existing instances
        try:
            old_instance = Application.objects.get(pk=instance.pk)
            
            # Check if status changed to approved
            if old_instance.status != 'approved' and instance.status == 'approved':
                instance.approved_at = timezone.now()
                # Email will be sent in post_save
                
            # Check if status changed to rejected
            elif old_instance.status != 'rejected' and instance.status == 'rejected':
                # Email will be sent in post_save
                pass
            
            # Check if document status changed
            if (old_instance.identity_document_status != instance.identity_document_status and 
                instance.identity_document_status in ['approved', 'rejected']):
                # Store the change to send email after save
                instance._document_status_changed = True
                
        except Application.DoesNotExist:
            pass

@receiver(post_save, sender=Application)
def handle_application_status_email(sender, instance, created, **kwargs):
    """Send status change emails"""
    if not created:  # Only for updates
        if instance.status == 'approved' and instance.approved_at:
            send_approval_email(instance.user, instance)
        elif instance.status == 'rejected':
            send_rejection_email(instance.user, instance, instance.rejection_reason or "Please review your application details.")
        
        # Send document review email if status changed
        if getattr(instance, '_document_status_changed', False):
            send_document_review_email(instance.user, instance)
            # Clean up the flag
            if hasattr(instance, '_document_status_changed'):
                delattr(instance, '_document_status_changed')