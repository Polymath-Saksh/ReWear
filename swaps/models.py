from django.db import models
from django.contrib.auth.models import User
from items.models import Item

class Swap(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='swaps_requested')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='swaps_received')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    offered_item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='swap_offers')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_point_redemption = models.BooleanField(default=False)
    points_used = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Swap: {self.item.title} ({self.status})"
