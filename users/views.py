from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import UserProfile
from .serializers import UserProfileSerializer, UserRegisterSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .forms import PasswordResetRequestForm, PasswordResetConfirmForm, UserSignupForm, UserLoginForm
from .email_service import azure_email_service
from .forms import UserSignupForm

# Template Views for HTML pages
class UserSignupView(View):
    template_name = 'users/signup.html'
    form_class = UserSignupForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {
            'form': form,
            'title': 'Sign Up - ReWear'
        })
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('users:login')
        return render(request, self.template_name, {
            'form': form,
            'title': 'Sign Up - ReWear'
        })

class UserLoginView(View):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {
            'form': form,
            'title': 'Login - ReWear'
        })
    
    def post(self, request):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            # Redirect to next page or dashboard
            next_page = request.GET.get('next', 'dashboard:dashboard')
            return redirect(next_page)
        return render(request, self.template_name, {
            'form': form,
            'title': 'Login - ReWear'
        })

class UserLogoutView(TemplateView):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('core:landing')

@method_decorator(login_required, name='dispatch')
class UserProfileTemplateView(TemplateView):
    template_name = 'users/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Profile - ReWear'
        context['user'] = self.request.user
        return context

@method_decorator(login_required, name='dispatch')
class UserEditProfileView(TemplateView):
    template_name = 'users/edit_profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Profile - ReWear'
        context['user'] = self.request.user
        return context

# API Views (keep existing for API functionality)
# User Registration Endpoint
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

# User Profile Retrieve/Update Endpoint
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Always return the profile for the currently authenticated user
        return self.request.user.userprofile # type: ignore

# Optionally, add a simple endpoint to get the authenticated user's info
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user.userprofile)
        return Response(serializer.data)

# Password Reset Views
class PasswordResetRequestView(TemplateView):
    """View for requesting password reset"""
    template_name = 'users/password_reset_request.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reset Password - ReWear'
        context['form'] = PasswordResetRequestForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                # Generate token and uidb64
                token = default_token_generator.make_token(user)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Build reset link
                reset_url = request.build_absolute_uri(
                    reverse('users:password_reset_confirm', kwargs={
                        'uidb64': uidb64,
                        'token': token
                    })
                )
                
                # Send email
                if azure_email_service.send_password_reset_email(user, reset_url):
                    messages.success(
                        request, 
                        'Password reset instructions have been sent to your email address.'
                    )
                    return redirect('users:password_reset_done')
                else:
                    messages.error(
                        request, 
                        'Failed to send email. Please try again later.'
                    )
        
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

class PasswordResetDoneView(TemplateView):
    """View shown after password reset email is sent"""
    template_name = 'users/password_reset_done.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Password Reset Sent - ReWear'
        return context

class PasswordResetConfirmView(TemplateView):
    """View for confirming password reset with token"""
    template_name = 'users/password_reset_confirm.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Set New Password - ReWear'
        
        # Get user from uidb64
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')
        user = self.get_user(uidb64)
        
        # Check if token is valid
        if user and default_token_generator.check_token(user, token):
            context['validlink'] = True
            context['form'] = PasswordResetConfirmForm(user)
            context['user'] = user
        else:
            context['validlink'] = False
            
        return context
    
    def get_user(self, uidb64):
        """Get user from uidb64"""
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user
    
    def post(self, request, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')
        user = self.get_user(uidb64)
        
        if user and default_token_generator.check_token(user, token):
            form = PasswordResetConfirmForm(user, request.POST)
            if form.is_valid():
                form.save()
                
                # Send confirmation email
                azure_email_service.send_password_reset_confirmation_email(user)
                
                messages.success(
                    request, 
                    'Your password has been reset successfully. You can now log in with your new password.'
                )
                return redirect('users:password_reset_complete')
        else:
            form = PasswordResetConfirmForm(user)
            messages.error(request, 'The password reset link is invalid or has expired.')
        
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

class PasswordResetCompleteView(TemplateView):
    """View shown after successful password reset"""
    template_name = 'users/password_reset_complete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Password Reset Complete - ReWear'
        return context
