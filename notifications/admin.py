from django.contrib import admin
from .models import Notification, Event, Announcement

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')
    readonly_fields = ('created_at',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'is_active', 'created_by', 'created_at')
    list_filter = ('is_active', 'date', 'created_at')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('created_at',)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'is_active', 'is_pinned', 'created_by', 'created_at')
    list_filter = ('priority', 'is_active', 'is_pinned', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at',)