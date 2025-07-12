from rest_framework import serializers
from .models import Item, ItemImage

class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ['id', 'image', 'is_primary', 'uploaded_at']

class ItemSerializer(serializers.ModelSerializer):
    images = ItemImageSerializer(many=True, read_only=True)
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Item
        fields = [
            'id', 'title', 'description', 'category', 'size', 'condition',
            'owner', 'owner_username', 'is_approved', 'is_available',
            'created_at', 'updated_at', 'tags', 'point_value', 'images'
        ]
        read_only_fields = ['owner', 'is_approved', 'created_at', 'updated_at', 'images', 'owner_username']
