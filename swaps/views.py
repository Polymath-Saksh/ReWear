from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Swap
from .serializers import SwapSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

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
