from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/applications/', include('applications.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/beneficiaries/', include('beneficiaries.urls')),
    path('api/admin/', include('admin_api.urls')),
    path('api/claims/', include('claims.urls')),
    path('api/notifications/', include('notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)