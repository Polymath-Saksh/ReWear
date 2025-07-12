from django.urls import path
from . import views

urlpatterns = [
    path('items/pending/', views.PendingItemListView.as_view(), name='pending-items'),
    path('items/<int:pk>/approve/', views.ApproveItemView.as_view(), name='approve-item'),
    path('items/<int:pk>/reject/', views.RejectItemView.as_view(), name='reject-item'),
    path('users/', views.UserListView.as_view(), name='user-list'),
]
