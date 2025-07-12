from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    # Admin Panel Web Views
    path('', views.admin_dashboard_view, name='dashboard'),  # Main admin panel
    path('login/', views.admin_login_view, name='login'),
    path('logout/', views.admin_logout_view, name='logout'),
    path('dashboard/', views.admin_dashboard_view, name='dashboard'),
    
    # API Endpoints for item management
    path('api/items/pending/', views.PendingItemListView.as_view(), name='pending-items'),
    path('api/items/<int:pk>/approve/', views.ApproveItemView.as_view(), name='approve-item'),
]
