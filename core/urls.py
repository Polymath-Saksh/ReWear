from django.urls import path
from . import views

urlpatterns = [
    path('settings/', views.SiteSettingList.as_view(), name='site-settings'),
    path('contact/', views.ContactMessageCreate.as_view(), name='contact-message'),
]
