from django.urls import path
from .views import DashboardTemplateView, ProfileTemplateView, UserDashboardView

app_name = 'dashboard'

urlpatterns = [
    # Template views for HTML pages
    path('', DashboardTemplateView.as_view(), name='dashboard'),
    path('profile/', ProfileTemplateView.as_view(), name='profile'),
    
    # API endpoints (keep for API functionality)
    path('api/', UserDashboardView.as_view(), name='api-dashboard'),
]
