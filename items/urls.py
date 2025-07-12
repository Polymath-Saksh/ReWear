from django.urls import path
from . import views

app_name = 'items'

urlpatterns = [
    path('', views.ItemListCreateView.as_view(), name='browse'),
    path('add/', views.ItemListCreateView.as_view(), name='add'),
    path('my-items/', views.ItemListCreateView.as_view(), name='my_items'),
    path('<int:pk>/', views.ItemDetailView.as_view(), name='detail'),
    path('<int:item_id>/images/', views.ItemImageUploadView.as_view(), name='item-image-upload'),
]
