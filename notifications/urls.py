from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.notifications_list, name='notifications_list'),
    path('announcements/', views.announcements_list, name='announcements_list'),
    path('announcements/create/', views.create_announcement, name='create_announcement'),
    path('events/', views.events_list, name='events_list'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/<int:event_id>/register/', views.register_for_event, name='register_for_event'),
    path('mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('<int:notification_id>/', views.mark_notification_read, name='mark_notification_read_patch'),
]