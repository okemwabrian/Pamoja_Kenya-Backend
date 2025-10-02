from django.contrib import admin
from .models import (
    Notification, Event, Announcement, EventRegistration,
    Meeting, ContactMessage, AdminNotification
)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'get_notification_type_display', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'user__email', 'title', 'message')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} notifications marked as read.')
    mark_as_read.short_description = 'Mark selected notifications as read'
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} notifications marked as unread.')
    mark_as_unread.short_description = 'Mark selected notifications as unread'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'is_active', 'is_featured', 'created_by', 'created_at')
    list_filter = ('is_active', 'is_featured', 'registration_required', 'date', 'created_at')
    search_fields = ('title', 'description', 'location', 'created_by__username')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'
    
    actions = ['activate_events', 'deactivate_events', 'feature_events']
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', 'date', 'end_date', 'location', 'image')
        }),
        ('Settings', {
            'fields': ('is_active', 'is_featured', 'registration_required', 'max_attendees')
        }),
        ('Management', {
            'fields': ('created_by',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def activate_events(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} events activated.')
    activate_events.short_description = 'Activate selected events'
    
    def deactivate_events(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} events deactivated.')
    deactivate_events.short_description = 'Deactivate selected events'
    
    def feature_events(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} events featured.')
    feature_events.short_description = 'Feature selected events'

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_priority_display', 'is_active', 'is_pinned', 'expires_at', 'created_by', 'created_at')
    list_filter = ('priority', 'is_active', 'is_pinned', 'created_at', 'expires_at')
    search_fields = ('title', 'content', 'created_by__username')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    actions = ['activate_announcements', 'deactivate_announcements', 'pin_announcements']
    
    fieldsets = (
        ('Announcement Information', {
            'fields': ('title', 'content', 'priority')
        }),
        ('Settings', {
            'fields': ('is_active', 'is_pinned', 'expires_at')
        }),
        ('Management', {
            'fields': ('created_by',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def activate_announcements(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} announcements activated.')
    activate_announcements.short_description = 'Activate selected announcements'
    
    def deactivate_announcements(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} announcements deactivated.')
    deactivate_announcements.short_description = 'Deactivate selected announcements'
    
    def pin_announcements(self, request, queryset):
        updated = queryset.update(is_pinned=True)
        self.message_user(request, f'{updated} announcements pinned.')
    pin_announcements.short_description = 'Pin selected announcements'

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'registered_at', 'attended')
    list_filter = ('attended', 'registered_at', 'event__date')
    search_fields = ('user__username', 'user__email', 'event__title', 'notes')
    readonly_fields = ('registered_at',)
    date_hierarchy = 'registered_at'
    
    actions = ['mark_as_attended', 'mark_as_not_attended']
    
    def mark_as_attended(self, request, queryset):
        updated = queryset.update(attended=True)
        self.message_user(request, f'{updated} registrations marked as attended.')
    mark_as_attended.short_description = 'Mark selected registrations as attended'
    
    def mark_as_not_attended(self, request, queryset):
        updated = queryset.update(attended=False)
        self.message_user(request, f'{updated} registrations marked as not attended.')
    mark_as_not_attended.short_description = 'Mark selected registrations as not attended'

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'type', 'duration', 'max_participants', 'created_by')
    list_filter = ('type', 'require_registration', 'send_notifications', 'date')
    search_fields = ('title', 'description', 'created_by__username')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'help_type', 'status', 'created_at')
    list_filter = ('help_type', 'status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    actions = ['mark_in_progress', 'mark_resolved']
    
    def mark_in_progress(self, request, queryset):
        updated = queryset.update(status='in_progress')
        self.message_user(request, f'{updated} messages marked as in progress.')
    mark_in_progress.short_description = 'Mark as in progress'
    
    def mark_resolved(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='resolved', resolved_at=timezone.now())
        self.message_user(request, f'{updated} messages marked as resolved.')
    mark_resolved.short_description = 'Mark as resolved'

@admin.register(AdminNotification)
class AdminNotificationAdmin(admin.ModelAdmin):
    list_display = ('type', 'title', 'priority', 'is_read', 'created_at')
    list_filter = ('type', 'priority', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'type')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    actions = ['mark_as_read']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} admin notifications marked as read.')
    mark_as_read.short_description = 'Mark as read'