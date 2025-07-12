from django.urls import path
from .views import UserDashboardView

app_name = 'dashboard'

urlpatterns = [
    path('', UserDashboardView.as_view(), name='dashboard'),
    path('profile/', UserDashboardView.as_view(), name='profile'),
]
