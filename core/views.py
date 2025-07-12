from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from rest_framework import generics
from .models import SiteSetting, ContactMessage
from .serializers import SiteSettingSerializer, ContactMessageSerializer

# Template Views
class LandingPageView(TemplateView):
    """
    Landing page view for ReWear platform.
    """
    template_name = 'core/landing.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Import models inside method to avoid circular imports
        from items.models import Item
        from swaps.models import Swap
        
        # Get dynamic statistics
        context['total_items'] = Item.objects.filter(is_approved=True, is_available=True).count()
        context['total_users'] = User.objects.filter(is_superuser=False).count()  # Exclude admin users
        context['total_swaps'] = Swap.objects.filter(status='completed').count()
        
        return context

# API Views
class SiteSettingList(generics.ListAPIView):
    """
    API endpoint to retrieve all site settings.
    """
    queryset = SiteSetting.objects.all()
    serializer_class = SiteSettingSerializer

class ContactMessageCreate(generics.CreateAPIView):
    """
    API endpoint to submit a contact message.
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
