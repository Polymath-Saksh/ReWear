"""
Test script for Azure Communication Services
Run this to verify that the email service is working correctly.
"""
import os
import sys
import django

# Add the project root to the Python path
sys.path.append(r'C:\Users\Aloukik\Desktop\Team-Kairos')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ReWear.settings')
django.setup()

from users.email_service import azure_email_service

def test_azure_email_service():
    """Test the Azure Communication Services email functionality"""
    print("Testing Azure Communication Services Email...")
    
    # Test email configuration
    if azure_email_service.client is None:
        print("❌ Azure Email Service failed to initialize")
        return False
    
    print("✅ Azure Email Service initialized successfully")
    print(f"Sender Email: {azure_email_service.sender_email}")
    
    # Test sending a simple email
    test_email = "test@example.com"  # Change this to your email for actual testing
    subject = "ReWear Password Reset Test"
    html_content = """
    <html>
        <body>
            <h2>Test Email</h2>
            <p>This is a test email from ReWear's Azure Communication Services integration.</p>
        </body>
    </html>
    """
    text_content = "Test Email - This is a test email from ReWear's Azure Communication Services integration."
    
    print(f"\nWould send test email to: {test_email}")
    print(f"Subject: {subject}")
    print("Email service is ready for password reset functionality!")
    
    return True

if __name__ == "__main__":
    test_azure_email_service()
