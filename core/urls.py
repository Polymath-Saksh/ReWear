from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Template views
    path('', views.LandingPageView.as_view(), name='landing'),
    
    # API endpoints
    path('api/settings/', views.SiteSettingList.as_view(), name='site-settings'),
    path('api/contact/', views.ContactMessageCreate.as_view(), name='contact-message'),
]
