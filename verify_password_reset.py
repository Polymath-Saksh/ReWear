#!/usr/bin/env python3
"""
Verification script for Azure Communication Services Password Reset functionality
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ReWear.settings')
django.setup()

from django.conf import settings
from django.contrib.auth.models import User
from django.test import RequestFactory
from users.email_service import AzureEmailService
from users.views import PasswordResetRequestView
import logging

def verify_azure_communication_services():
    """Verify Azure Communication Services configuration"""
    print("🔄 Verifying Azure Communication Services Configuration...")
    
    # Check settings
    required_settings = [
        'AZURE_COMMUNICATION_CONNECTION_STRING',
        'AZURE_COMMUNICATION_SENDER_EMAIL'
    ]
    
    for setting in required_settings:
        if hasattr(settings, setting):
            value = getattr(settings, setting)
            if value:
                print(f"✅ {setting}: Configured")
            else:
                print(f"❌ {setting}: Not set")
                return False
        else:
            print(f"❌ {setting}: Not found in settings")
            return False
    
    # Test Azure Email Service initialization
    try:
        email_service = AzureEmailService()
        print("✅ Azure Email Service: Initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Azure Email Service initialization failed: {e}")
        return False

def verify_password_reset_urls():
    """Verify password reset URL configuration"""
    print("\n🔄 Verifying Password Reset URLs...")
    
    from django.urls import reverse
    
    url_names = [
        ('users:password_reset', 'password_reset'),
        ('users:password_reset_done', 'password_reset_done'),
        ('users:password_reset_confirm', 'password_reset_confirm'),
        ('users:password_reset_complete', 'password_reset_complete')
    ]
    
    for url_name, display_name in url_names:
        try:
            if 'password_reset_confirm' in url_name:
                # This URL requires parameters
                url = reverse(url_name, kwargs={'uidb64': 'test', 'token': 'test'})
            else:
                url = reverse(url_name)
            print(f"✅ {display_name}: {url}")
        except Exception as e:
            print(f"❌ {display_name}: URL reverse failed - {e}")
            return False
    
    return True

def verify_email_templates():
    """Verify email templates exist"""
    print("\n🔄 Verifying Email Templates...")
    
    from django.template.loader import get_template
    
    templates = [
        'emails/password_reset_subject.txt',
        'emails/password_reset_message.txt',
        'emails/password_reset_message.html',
        'emails/password_reset_confirmation_subject.txt',
        'emails/password_reset_confirmation_message.txt',
        'emails/password_reset_confirmation_message.html'
    ]
    
    for template in templates:
        try:
            get_template(template)
            print(f"✅ {template}: Found")
        except Exception as e:
            print(f"❌ {template}: Not found - {e}")
            return False
    
    return True

def verify_password_reset_templates():
    """Verify password reset HTML templates"""
    print("\n🔄 Verifying Password Reset HTML Templates...")
    
    from django.template.loader import get_template
    
    templates = [
        'users/password_reset_request.html',
        'users/password_reset_done.html',
        'users/password_reset_confirm.html',
        'users/password_reset_complete.html'
    ]
    
    for template in templates:
        try:
            get_template(template)
            print(f"✅ {template}: Found")
        except Exception as e:
            print(f"❌ {template}: Not found - {e}")
            return False
    
    return True

def main():
    """Main verification function"""
    print("🚀 Starting Azure Communication Services Password Reset Verification\n")
    
    verifications = [
        verify_azure_communication_services,
        verify_password_reset_urls,
        verify_email_templates,
        verify_password_reset_templates
    ]
    
    all_passed = True
    for verification in verifications:
        if not verification():
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL VERIFICATIONS PASSED!")
        print("✅ Azure Communication Services Password Reset is ready!")
        print("\n📋 Next Steps:")
        print("1. Start Django server: python manage.py runserver")
        print("2. Visit: http://127.0.0.1:8000/users/login/")
        print("3. Click 'Forgot Password?' link")
        print("4. Enter email address and test the flow")
        print("5. Check your email for password reset instructions")
    else:
        print("❌ SOME VERIFICATIONS FAILED!")
        print("Please check the errors above and fix them before testing.")
    print("="*60)

if __name__ == "__main__":
    main()
