from django.contrib import admin
from .models import Swap

@admin.register(Swap)
class SwapAdmin(admin.ModelAdmin):
    list_display = (
        'item', 'requester', 'owner', 'status',
        'is_point_redemption', 'points_used', 'created_at', 'updated_at'
    )
    list_filter = ('status', 'is_point_redemption', 'created_at')
    search_fields = ('item__title', 'requester__username', 'owner__username')
    readonly_fields = ('created_at', 'updated_at')
