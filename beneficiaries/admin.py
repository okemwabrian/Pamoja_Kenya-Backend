from django.contrib import admin
from .models import Beneficiary, BeneficiaryChangeRequest

@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'relationship', 'percentage', 'is_primary', 'is_active', 'user')
    list_filter = ('relationship', 'is_primary', 'is_active', 'created_at')
    search_fields = ('name', 'email', 'phone', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Beneficiary Info', {
            'fields': ('user', 'name', 'relationship', 'percentage', 'is_primary', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'date_of_birth')
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'state', 'zip_code', 'country')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(BeneficiaryChangeRequest)
class BeneficiaryChangeRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'status', 'created_at', 'processed_at', 'user')
    list_filter = ('status', 'created_at', 'processed_at')
    search_fields = ('full_name', 'email', 'current_names', 'new_names')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Request Info', {
            'fields': ('user', 'status', 'full_name', 'email')
        }),
        ('Change Details', {
            'fields': ('current_names', 'new_names')
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'state', 'zip_code')
        }),
        ('Processing Info', {
            'fields': ('admin_notes', 'processed_at', 'processed_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if change and obj.status in ['approved', 'rejected'] and not obj.processed_by:
            obj.processed_by = request.user
            from django.utils import timezone
            obj.processed_at = timezone.now()
        super().save_model(request, obj, form, change)