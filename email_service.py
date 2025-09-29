from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_welcome_email(user_email, user_name):
        """Send welcome email to new users"""
        try:
            subject = 'Welcome to Pamoja Kenya MN!'
            
            html_content = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 2rem; text-align: center; color: white;">
                    <h1>Welcome to Pamoja Kenya MN!</h1>
                </div>
                <div style="padding: 2rem; background: #f8f9fa;">
                    <h2>Hello {user_name},</h2>
                    <p>Thank you for joining our community! We're excited to have you as part of the Pamoja Kenya MN family.</p>
                    
                    <div style="background: white; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
                        <h3>What's Next?</h3>
                        <ul>
                            <li>Complete your membership application</li>
                            <li>Explore our services and benefits</li>
                            <li>Connect with other members</li>
                            <li>Stay updated with our announcements</li>
                        </ul>
                    </div>
                    
                    <p>If you have any questions, feel free to contact our support team.</p>
                    <p>Best regards,<br>The Pamoja Kenya MN Team</p>
                </div>
            </div>
            """
            
            text_content = strip_tags(html_content)
            
            msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            logger.info(f"Welcome email sent to {user_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send welcome email to {user_email}: {str(e)}")
            return False
    
    @staticmethod
    def send_payment_confirmation(user_email, user_name, payment_details):
        """Send payment confirmation email"""
        try:
            subject = 'Payment Confirmation - Pamoja Kenya MN'
            
            html_content = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background: #27ae60; padding: 2rem; text-align: center; color: white;">
                    <h1>Payment Confirmed!</h1>
                </div>
                <div style="padding: 2rem; background: #f8f9fa;">
                    <h2>Hello {user_name},</h2>
                    <p>Your payment has been successfully processed.</p>
                    
                    <div style="background: white; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
                        <h3>Payment Details:</h3>
                        <p><strong>Amount:</strong> ${payment_details.get('amount', 'N/A')}</p>
                        <p><strong>Method:</strong> {payment_details.get('method', 'N/A')}</p>
                        <p><strong>Transaction ID:</strong> {payment_details.get('transaction_id', 'N/A')}</p>
                        <p><strong>Date:</strong> {payment_details.get('date', 'N/A')}</p>
                    </div>
                    
                    <p>Thank you for your payment!</p>
                    <p>Best regards,<br>The Pamoja Kenya MN Team</p>
                </div>
            </div>
            """
            
            text_content = strip_tags(html_content)
            
            msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            logger.info(f"Payment confirmation email sent to {user_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send payment confirmation to {user_email}: {str(e)}")
            return False
    
    @staticmethod
    def send_application_status_email(user_email, user_name, status, application_type):
        """Send application status update email"""
        try:
            status_colors = {
                'approved': '#27ae60',
                'rejected': '#e74c3c',
                'pending': '#f39c12'
            }
            
            subject = f'Application {status.title()} - Pamoja Kenya MN'
            
            html_content = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background: {status_colors.get(status, '#667eea')}; padding: 2rem; text-align: center; color: white;">
                    <h1>Application {status.title()}</h1>
                </div>
                <div style="padding: 2rem; background: #f8f9fa;">
                    <h2>Hello {user_name},</h2>
                    <p>Your {application_type} application has been <strong>{status}</strong>.</p>
                    
                    <div style="background: white; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
                        <h3>Next Steps:</h3>
                        {'<p>Congratulations! Please proceed with the next steps in your member portal.</p>' if status == 'approved' else ''}
                        {'<p>Please review your application and contact us if you have questions.</p>' if status == 'rejected' else ''}
                        {'<p>Your application is being reviewed. We will notify you once a decision is made.</p>' if status == 'pending' else ''}
                    </div>
                    
                    <p>Best regards,<br>The Pamoja Kenya MN Team</p>
                </div>
            </div>
            """
            
            text_content = strip_tags(html_content)
            
            msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            logger.info(f"Application status email sent to {user_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send application status email to {user_email}: {str(e)}")
            return False