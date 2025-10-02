from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from missing_views import profile, stats, password_reset, admin_stats
from accounts.views import notifications_list, notifications_events, notifications_announcements, activities_view
from accounts.dashboard_views import dashboard_stats, dashboard_activities
from api_root import api_root

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/applications/', include('applications.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/beneficiaries/', include('beneficiaries.urls')),
    path('api/admin/', include('admin_api.urls')),
    path('api/claims/', include('claims.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/', api_root, name='api_root'),
    # Dashboard endpoints
    path('api/dashboard/stats/', dashboard_stats, name='dashboard_stats'),
    path('api/dashboard/activities/', dashboard_activities, name='dashboard_activities'),
    # Direct endpoints for frontend compatibility
    path('api/events/', include('notifications.urls')),
    path('api/announcements/', include('notifications.urls')),
    # Missing endpoints fix
    path('api/auth/profile/', profile, name='profile_fix'),
    path('api/auth/stats/', stats, name='stats_fix'),
    path('api/auth/password-reset/', password_reset, name='password_reset_fix'),
    path('api/admin/stats/', admin_stats, name='admin_stats_fix'),
    # Notification endpoints
    path('api/notifications/list/', notifications_list, name='notifications_list_main'),
    path('api/notifications/events/', notifications_events, name='notifications_events_main'),
    path('api/notifications/announcements/', notifications_announcements, name='notifications_announcements_main'),
    path('api/activities/', activities_view, name='activities_main'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)