from django.urls import path
from . import views

urlpatterns = [
    # Dashboard & Stats
    path('stats/', views.admin_dashboard_stats, name='admin_dashboard_stats'),
    path('dashboard-stats/', views.admin_dashboard_stats, name='admin_dashboard_stats_alt'),
    path('recent-activities/', views.recent_activities, name='recent_activities'),
    
    # User Management
    path('users/', views.users_list, name='users_list'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/<int:user_id>/make-admin/', views.make_user_admin, name='make_user_admin'),
    
    # Application Management
    path('applications/', views.applications_list, name='applications_list'),
    path('applications/<int:app_id>/update-status/', views.update_application_status, name='update_application_status'),
    path('applications/<int:app_id>/documents/', views.get_application_documents, name='get_application_documents'),
    
    # Claims Management
    path('claims/', views.admin_claims_list, name='admin_claims_list'),
    path('claims/<int:claim_id>/', views.admin_update_claim_status, name='admin_update_claim_status'),
    
    # Payment Management
    path('payments/', views.admin_payments_list, name='admin_payments_list'),
    
    # Content Management
    # Content Management - Announcements
    path('announcements/', views.admin_announcements_list, name='admin_announcements_list'),
    path('announcements/create/', views.create_announcement, name='create_announcement'),
    path('announcements/<int:announcement_id>/', views.admin_update_announcement, name='admin_update_announcement'),
    path('announcements/<int:announcement_id>/delete/', views.admin_delete_announcement, name='admin_delete_announcement'),
    
    # Content Management - Events
    path('events/', views.admin_events_list, name='admin_events_list'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/<int:event_id>/', views.admin_update_event, name='admin_update_event'),
    path('events/<int:event_id>/delete/', views.admin_delete_event, name='admin_delete_event'),
    
    # Content Management - Meetings
    path('meetings/', views.admin_meetings_list, name='admin_meetings_list'),
    path('meetings/create/', views.create_meeting, name='create_meeting'),
    path('meetings/<int:meeting_id>/', views.admin_update_meeting, name='admin_update_meeting'),
    path('meetings/<int:meeting_id>/delete/', views.admin_delete_meeting, name='admin_delete_meeting'),
    
    # Contact Messages Management
    path('contacts/', views.admin_contacts_list, name='admin_contacts_list'),
    path('contacts/<int:contact_id>/', views.admin_update_contact, name='admin_update_contact'),
    
    # Document endpoints
    path('claims/<int:claim_id>/documents/', views.get_claim_documents, name='get_claim_documents'),
]