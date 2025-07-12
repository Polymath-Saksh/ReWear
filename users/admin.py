from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'location', 'is_verified', 'joined_date')
    search_fields = ('user__username', 'user__email', 'location')
    list_filter = ('is_verified', 'joined_date')
