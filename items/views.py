from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Item, ItemImage
from .serializers import ItemSerializer, ItemImageSerializer
from rest_framework.permissions import IsAuthenticated

# Web Views for Templates
def browse_items_view(request):
    """Display all available items with filtering and search"""
    items = Item.objects.filter(is_approved=True, is_available=True).order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        items = items.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(brand__icontains=search_query)
        )
    
    # Category filtering
    category_filter = request.GET.get('category', '')
    if category_filter:
        items = items.filter(category=category_filter)
    
    # Size filtering
    size_filter = request.GET.get('size', '')
    if size_filter:
        items = items.filter(size=size_filter)
    
    # Condition filtering
    condition_filter = request.GET.get('condition', '')
    if condition_filter:
        items = items.filter(condition=condition_filter)
    
    # Pagination
    paginator = Paginator(items, 12)  # Show 12 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options for the form
    categories = Item.objects.values_list('category', flat=True).distinct()
    sizes = Item.objects.values_list('size', flat=True).distinct()
    conditions = Item.objects.values_list('condition', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'category_filter': category_filter,
        'size_filter': size_filter,
        'condition_filter': condition_filter,
        'categories': categories,
        'sizes': sizes,
        'conditions': conditions,
        'total_items': items.count(),
    }
    
    return render(request, 'items/browse.html', context)

def item_detail_view(request, item_id):
    """Display single item detail"""
    item = get_object_or_404(Item, id=item_id, is_approved=True)
    related_items = Item.objects.filter(
        category=item.category,
        is_approved=True,
        is_available=True
    ).exclude(pk=item.pk)[:4]
    
    context = {
        'item': item,
        'related_items': related_items,
    }
    return render(request, 'items/detail.html', context)

@login_required
def add_item_view(request):
    """Add new item form"""
    if request.method == 'POST':
        # Handle form submission
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        size = request.POST.get('size')
        condition = request.POST.get('condition')
        point_value = request.POST.get('point_value', 10)
        
        # Create the item
        item = Item.objects.create(
            owner=request.user,
            title=title,
            description=description,
            category=category,
            size=size,
            condition=condition,
            point_value=int(point_value) if point_value else 10,
            is_approved=True  # Auto-approve for hackathon
        )
        
        messages.success(request, 'Item listed successfully!')
        return redirect('items:detail', item_id=item.pk)
    
    context = {
        'categories': Item.CATEGORY_CHOICES,
        'conditions': Item.CONDITION_CHOICES,
    }
    return render(request, 'items/add.html', context)

@login_required
def my_items_view(request):
    """Display user's own items"""
    items = Item.objects.filter(owner=request.user).order_by('-created_at')
    
    context = {
        'items': items,
    }
    return render(request, 'items/my_items.html', context)

# API Views for REST endpoints
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
