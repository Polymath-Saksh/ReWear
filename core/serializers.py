from rest_framework import serializers
from .models import SiteSetting, ContactMessage

class SiteSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        fields = ['key', 'value']

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message', 'created_at']
        read_only_fields = ['created_at']
