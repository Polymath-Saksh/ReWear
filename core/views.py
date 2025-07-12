from django.shortcuts import render
from django.views.generic import TemplateView
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
        # Add any context data for the landing page
        context['featured_items'] = []  # Will be populated later
        context['total_users'] = 0  # Will be populated later
        context['total_swaps'] = 0  # Will be populated later
        context['items_saved'] = 0  # Will be populated later
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
