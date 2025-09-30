from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile_view, name='update_profile'),
    path('stats/', views.user_stats_view, name='user_stats'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('contact/', views.contact_form, name='contact_form'),
]