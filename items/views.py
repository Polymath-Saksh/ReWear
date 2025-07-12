from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Item, ItemImage
from .serializers import ItemSerializer, ItemImageSerializer
from rest_framework.permissions import IsAuthenticated

# List all approved and available items, or create a new item
class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.filter(is_approved=True, is_available=True)
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Retrieve, update, or delete a specific item (owner only for update/delete)
class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Owners can access their own items; others see only approved items
        if self.request.user.is_authenticated:
            return Item.objects.filter(owner=self.request.user) | Item.objects.filter(is_approved=True)
        return Item.objects.filter(is_approved=True)

    def perform_update(self, serializer):
        # Only the owner can update
        if self.request.user != self.get_object().owner:
            raise PermissionDenied("You do not have permission to edit this item.")
        serializer.save()

    def perform_destroy(self, instance):
        # Only the owner can delete
        if self.request.user != instance.owner:
            raise PermissionDenied("You do not have permission to delete this item.")
        instance.delete()

# Upload images for an item
class ItemImageUploadView(generics.CreateAPIView):
    serializer_class = ItemImageSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        item_id = self.kwargs.get('item_id')
        item = Item.objects.get(pk=item_id)
        if item.owner != request.user:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(item=item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
