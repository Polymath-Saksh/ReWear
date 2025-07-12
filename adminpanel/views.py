from rest_framework import generics, permissions, status
from rest_framework.response import Response
from items.models import Item
from items.serializers import ItemSerializer
from django.contrib.auth.models import User
from users.serializers import UserProfileSerializer
from rest_framework.permissions import IsAdminUser

# List all pending items for approval
class PendingItemListView(generics.ListAPIView):
    queryset = Item.objects.filter(is_approved=False)
    serializer_class = ItemSerializer
    permission_classes = [IsAdminUser]

# Approve an item (PATCH request)
class ApproveItemView(generics.UpdateAPIView):
    queryset = Item.objects.filter(is_approved=False)
    serializer_class = ItemSerializer
    permission_classes = [IsAdminUser]

    def patch(self, request, *args, **kwargs):
        item = self.get_object()
        item.is_approved = True
        item.save()
        return Response(ItemSerializer(item).data)

# Reject (delete) an item
class RejectItemView(generics.DestroyAPIView):
    queryset = Item.objects.filter(is_approved=False)
    serializer_class = ItemSerializer
    permission_classes = [IsAdminUser]

# List all users (optional)
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]
