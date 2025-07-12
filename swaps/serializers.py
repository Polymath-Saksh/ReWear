from rest_framework import serializers
from .models import Swap

class SwapSerializer(serializers.ModelSerializer):
    requester_username = serializers.CharField(source='requester.username', read_only=True)
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    item_title = serializers.CharField(source='item.title', read_only=True)
    offered_item_title = serializers.CharField(source='offered_item.title', read_only=True, default=None)

    class Meta:
        model = Swap
        fields = [
            'id', 'requester', 'requester_username', 'owner', 'owner_username',
            'item', 'item_title', 'offered_item', 'offered_item_title',
            'status', 'is_point_redemption', 'points_used',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'status', 'created_at', 'updated_at',
            'requester_username', 'owner_username', 'item_title', 'offered_item_title'
        ]
