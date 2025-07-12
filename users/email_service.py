"""
Email service using Azure Communication Services
"""
import logging
from azure.communication.email import EmailClient
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from typing import Optional

logger = logging.getLogger(__name__)

class AzureEmailService:
    def __init__(self):
        """Initialize Azure Communication Services Email Client"""
        try:
            self.client = EmailClient.from_connection_string(settings.AZURE_COMMUNICATION_CONNECTION_STRING)
            self.sender_email = settings.AZURE_COMMUNICATION_SENDER_EMAIL
        except Exception as e:
            logger.error(f"Failed to initialize Azure Email Service: {e}")
            self.client = None
            self.sender_email = None

    def send_email(self, to_email: str, subject: str, html_content: str, text_content: Optional[str] = None) -> bool:
        """
        Send email using Azure Communication Services
        
        Args:
            to_email (str): Recipient email address
            subject (str): Email subject
            html_content (str): HTML content of the email
            text_content (str, optional): Plain text content. If not provided, will strip HTML
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        if not self.client:
            logger.error("Azure Email Service not properly initialized")
            return False
            
        try:
            # Create text content if not provided
            if not text_content:
                text_content = strip_tags(html_content)
            
            message = {
                "senderAddress": self.sender_email,
                "recipients": {
                    "to": [{"address": to_email}],
                },
                "content": {
                    "subject": subject,
                    "plainText": text_content,
                    "html": html_content
                }
            }
            
            # Send the email
            poller = self.client.begin_send(message)
            result = poller.result()
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False

    def send_password_reset_email(self, user, reset_link: str) -> bool:
        """
        Send password reset email to user
        
        Args:
            user: Django User object
            reset_link (str): Password reset link
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Render email template
            context = {
                'user': user,
                'reset_link': reset_link,
                'site_name': 'ReWear',
                'site_url': 'http://127.0.0.1:8000',  # Update with your domain
            }
            
            html_content = render_to_string('emails/password_reset.html', context)
            text_content = render_to_string('emails/password_reset.txt', context)
            
            subject = "Reset Your ReWear Password"
            
            return self.send_email(
                to_email=user.email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
        except Exception as e:
            logger.error(f"Failed to send password reset email to {user.email}: {e}")
            return False

    def send_password_reset_confirmation_email(self, user) -> bool:
        """
        Send password reset confirmation email to user
        
        Args:
            user: Django User object
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            context = {
                'user': user,
                'site_name': 'ReWear',
                'site_url': 'http://127.0.0.1:8000',
            }
            
            html_content = render_to_string('emails/password_reset_confirmation.html', context)
            text_content = render_to_string('emails/password_reset_confirmation.txt', context)
            
            subject = "Your ReWear Password Has Been Reset"
            
            return self.send_email(
                to_email=user.email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
        except Exception as e:
            logger.error(f"Failed to send password reset confirmation email to {user.email}: {e}")
            return False

# Global instance
azure_email_service = AzureEmailService()
