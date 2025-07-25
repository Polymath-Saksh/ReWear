"""
URL configuration for ReWear project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    
    # App URLs
    path("", include("core.urls")),  # Landing page and core functionality
    path("users/", include("users.urls")),  # User management
    path("items/", include("items.urls")),  # Item management
    path("swaps/", include("swaps.urls")),  # Swap functionality
    path("dashboard/", include("dashboard.urls")),  # User dashboard
    path("adminpanel/", include("adminpanel.urls")),  # Admin panel
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
