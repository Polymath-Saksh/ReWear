from rest_framework import generics
from .models import SiteSetting, ContactMessage
from .serializers import SiteSettingSerializer, ContactMessageSerializer

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
