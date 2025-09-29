from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'application_type', 'status', 'amount', 'created_at', 'user')
    list_filter = ('application_type', 'status', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Application Info', {
            'fields': ('user', 'application_type', 'status', 'amount')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth')
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'state', 'zip_code', 'country')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship')
        }),
        ('Employment Information', {
            'fields': ('occupation', 'employer', 'annual_income')
        }),
        ('Additional Information', {
            'fields': ('notes', 'admin_notes')
        }),
        ('Approval Information', {
            'fields': ('approved_at', 'approved_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if change and obj.status == 'approved' and not obj.approved_by:
            obj.approved_by = request.user
            from django.utils import timezone
            obj.approved_at = timezone.now()
        super().save_model(request, obj, form, change)