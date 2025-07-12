from django.urls import path
from . import views

app_name = 'items'

urlpatterns = [
    # Web Views
    path('', views.browse_items_view, name='browse'),
    path('add/', views.add_item_view, name='add'),
    path('my-items/', views.my_items_view, name='my_items'),
    path('<int:item_id>/', views.item_detail_view, name='detail'),
    
    # API Views
    path('api/', views.ItemListCreateView.as_view(), name='api-list'),
    path('api/<int:pk>/', views.ItemDetailView.as_view(), name='api-detail'),
]
