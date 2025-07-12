from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from items.models import Item
from items.serializers import ItemSerializer
from users.serializers import UserProfileSerializer
from rest_framework.permissions import IsAdminUser
from swaps.models import Swap

def is_admin(user):
    return user.is_authenticated and user.is_staff

def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('adminpanel:dashboard')
        else:
            messages.error(request, 'Invalid admin credentials or insufficient privileges.')
    
    return render(request, 'adminpanel/login.html')

@user_passes_test(is_admin)
def admin_dashboard_view(request):
    context = {
        'total_users': User.objects.count(),
        'total_items': Item.objects.count(),
        'active_swaps': Swap.objects.filter(status='pending').count(),
        'pending_items': Item.objects.filter(is_approved=False).count(),
        'pending_items_list': Item.objects.filter(is_approved=False).order_by('-created_at')[:10],
        'users_list': User.objects.all().order_by('-date_joined')[:20],
    }
    return render(request, 'adminpanel/admin_panel.html', context)

@user_passes_test(is_admin)
def admin_users_view(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'adminpanel/admin_panel.html', {'users': users})

@user_passes_test(is_admin)
def admin_items_view(request):
    items = Item.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/admin_panel.html', {'items': items})

@user_passes_test(is_admin)
def admin_swaps_view(request):
    swaps = Swap.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/admin_panel.html', {'swaps': swaps})

def admin_logout_view(request):
    logout(request)
    return redirect('adminpanel:login')

# API Views for REST endpoints
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
