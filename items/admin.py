from django.contrib import admin
from .models import Item, ItemImage

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'owner', 'category', 'condition', 'is_approved',
        'is_available', 'created_at'
    )
    list_filter = ('category', 'condition', 'is_approved', 'is_available', 'created_at')
    search_fields = ('title', 'description', 'owner__username')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['approve_items', 'reject_items']

    def approve_items(self, request, queryset):
        queryset.update(is_approved=True)
    approve_items.short_description = "Approve selected items"

    def reject_items(self, request, queryset):
        queryset.update(is_approved=False)
    reject_items.short_description = "Reject selected items"

@admin.register(ItemImage)
class ItemImageAdmin(admin.ModelAdmin):
    list_display = ('item', 'is_primary', 'uploaded_at')
    list_filter = ('is_primary', 'uploaded_at')
    search_fields = ('item__title',)
