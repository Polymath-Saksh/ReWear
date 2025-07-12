from django.urls import path
from . import views

app_name = 'swaps'

urlpatterns = [
    path('', views.SwapListCreateView.as_view(), name='my_swaps'),
    path('<int:pk>/', views.SwapDetailView.as_view(), name='detail'),
]
