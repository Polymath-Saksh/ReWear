from django.urls import path
from . import views

urlpatterns = [
    path('', views.SwapListCreateView.as_view(), name='swap-list-create'),
    path('<int:pk>/', views.SwapDetailView.as_view(), name='swap-detail'),
]
