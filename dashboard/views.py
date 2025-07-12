from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserProfileSerializer
from items.serializers import ItemSerializer
from swaps.serializers import SwapSerializer
from items.serializers import ItemSerializer
from swaps.serializers import SwapSerializer

@method_decorator(login_required, name='dispatch')
class DashboardTemplateView(TemplateView):
    template_name = 'dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get user's items and swaps
        try:
            from items.models import Item
            user_items = Item.objects.filter(owner=self.request.user)[:5]  # Latest 5 items
        except:
            user_items = []
            
        user_swaps = []
        
        # Try to get swaps if the model exists
        try:
            from swaps.models import Swap
            user_swaps = Swap.objects.filter(
                models.Q(requester=self.request.user) | models.Q(owner=self.request.user)
            )[:5]
        except:
            pass
        
        context['user_items'] = user_items
        context['user_swaps'] = user_swaps
        context['total_items'] = len(user_items)
        context['total_swaps'] = len(user_swaps)
        context['title'] = 'Dashboard - ReWear'
        
        return context

@method_decorator(login_required, name='dispatch')
class ProfileTemplateView(TemplateView):
    template_name = 'dashboard/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Profile - ReWear'
        return context

# Keep API Views for API functionality
class UserDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = request.user.userprofile
        user_items = request.user.items.all()
        user_swaps_requested = request.user.swaps_requested.all()
        user_swaps_received = request.user.swaps_received.all()

        profile_data = UserProfileSerializer(user_profile).data
        items_data = ItemSerializer(user_items, many=True).data
        swaps_requested_data = SwapSerializer(user_swaps_requested, many=True).data
        swaps_received_data = SwapSerializer(user_swaps_received, many=True).data

        return Response({
            "profile": profile_data,
            "items": items_data,
            "swaps_requested": swaps_requested_data,
            "swaps_received": swaps_received_data,
        })
