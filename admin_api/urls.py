from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.admin_dashboard_stats, name='admin_dashboard_stats'),
    path('dashboard-stats/', views.admin_dashboard_stats, name='admin_dashboard_stats_alt'),
    path('recent-activities/', views.recent_activities, name='recent_activities'),
    path('users/', views.users_list, name='users_list'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('applications/', views.applications_list, name='applications_list'),
    path('applications/<int:app_id>/update-status/', views.update_application_status, name='update_application_status'),
    path('create-announcement/', views.create_announcement, name='create_announcement'),
    path('create-event/', views.create_event, name='create_event'),
]