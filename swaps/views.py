from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.db import models
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Swap
from .serializers import SwapSerializer
from rest_framework.permissions import IsAuthenticated

# Template Views
@method_decorator(login_required, name='dispatch')
class MySwapsTemplateView(TemplateView):
    template_name = 'swaps/my_swaps.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get user's swaps
        user_swaps = []
        try:
            user_swaps = Swap.objects.filter(
                models.Q(requester=self.request.user) | models.Q(owner=self.request.user)
            ).order_by('-created_at')
        except:
            pass
        
        context['swaps'] = user_swaps
        context['title'] = 'My Swaps - ReWear'
        return context

# API Views
# List all swaps for the authenticated user, or create a new swap request
class SwapListCreateView(generics.ListCreateAPIView):
    serializer_class = SwapSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Show swaps where the user is requester or owner
        return Swap.objects.filter(
            requester=self.request.user
        ) | Swap.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)

# Retrieve or update a specific swap (status change)
class SwapDetailView(generics.RetrieveUpdateAPIView):
    queryset = Swap.objects.all()
    serializer_class = SwapSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only allow involved users to access the swap
        return Swap.objects.filter(
            requester=self.request.user
        ) | Swap.objects.filter(owner=self.request.user)

    def perform_update(self, serializer):
        swap = self.get_object()
        # Only the owner can accept/reject/cancel
        if self.request.user != swap.item.owner and self.request.user != swap.requester:
            raise permissions.PermissionDenied("You don't have permission to update this swap.")
        serializer.save()
