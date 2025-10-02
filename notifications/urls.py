from django.urls import path
from . import views

urlpatterns = [
    # Public endpoints (no auth required)
    path('announcements/', views.public_announcements, name='public_announcements'),
    path('events/', views.public_events, name='public_events'),
    path('meetings/', views.public_meetings, name='public_meetings'),
    
    # Protected endpoints (auth required)
    path('user/', views.user_notifications, name='user_notifications'),
    path('mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    
    # Legacy endpoints
    path('list/', views.notifications_list, name='notifications_list'),
    path('announcements/create/', views.create_announcement, name='create_announcement'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/<int:event_id>/register/', views.register_for_event, name='register_for_event'),
    path('<int:notification_id>/', views.mark_notification_read, name='mark_notification_read_patch'),
    
    # Contact System
    path('contact/submit/', views.submit_contact, name='submit_contact'),
    path('admin/contacts/', views.admin_contacts_list, name='admin_contacts_list'),
    path('admin/contacts/<int:contact_id>/', views.admin_update_contact, name='admin_update_contact'),
    path('admin/notifications/', views.admin_notifications_list, name='admin_notifications_list'),
    path('admin/notifications/send/', views.send_admin_notification, name='send_admin_notification'),
]