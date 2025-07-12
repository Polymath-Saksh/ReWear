from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import UserProfile
from .serializers import UserProfileSerializer, UserRegisterSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

# Template Views for HTML pages
class UserSignupView(TemplateView):
    template_name = 'users/signup.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign Up - ReWear'
        return context

class UserLoginView(TemplateView):
    template_name = 'users/login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login - ReWear'
        return context

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
        return self.request.user.userprofile

# Optionally, add a simple endpoint to get the authenticated user's info
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user.userprofile)
        return Response(serializer.data)
