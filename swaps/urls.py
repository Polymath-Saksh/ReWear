from django.urls import path
from . import views

app_name = 'swaps'

urlpatterns = [
    # Template views
    path('my-swaps/', views.MySwapsTemplateView.as_view(), name='my_swaps'),
    
    # API views
    path('api/', views.SwapListCreateView.as_view(), name='api-list'),
    path('api/<int:pk>/', views.SwapDetailView.as_view(), name='api-detail'),
]
