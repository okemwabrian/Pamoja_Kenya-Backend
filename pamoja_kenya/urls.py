from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from missing_views import profile, stats, password_reset, admin_stats

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/applications/', include('applications.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/beneficiaries/', include('beneficiaries.urls')),
    path('api/admin/', include('admin_api.urls')),
    path('api/claims/', include('claims.urls')),
    path('api/notifications/', include('notifications.urls')),
    # Direct endpoints for frontend compatibility
    path('api/events/', include('notifications.urls')),
    path('api/announcements/', include('notifications.urls')),
    # Missing endpoints fix
    path('api/auth/profile/', profile, name='profile_fix'),
    path('api/auth/stats/', stats, name='stats_fix'),
    path('api/auth/password-reset/', password_reset, name='password_reset_fix'),
    path('api/admin/stats/', admin_stats, name='admin_stats_fix'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)