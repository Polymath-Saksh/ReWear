from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Template views for HTML pages
    path('signup/', views.UserSignupView.as_view(), name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/', views.UserProfileTemplateView.as_view(), name='profile'),
    path('profile/edit/', views.UserEditProfileView.as_view(), name='edit_profile'),
    
    # API endpoints (keep for API functionality)
    path('api/register/', views.UserRegisterView.as_view(), name='api-register'),
    path('api/profile/', views.UserProfileView.as_view(), name='api-profile'),
    path('api/me/', views.CurrentUserView.as_view(), name='api-current-user'),
]
