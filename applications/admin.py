from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'get_application_type_display', 'get_status_display', 'get_identity_document_status_display', 'has_documents', 'amount', 'created_at', 'user')
    list_filter = ('application_type', 'status', 'identity_document_status', 'created_at', 'approved_at', 'documents_reviewed_at')
    search_fields = ('first_name', 'middle_name', 'last_name', 'email', 'phone', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    def has_documents(self, obj):
        return bool(obj.identity_document)
    has_documents.boolean = True
    has_documents.short_description = 'Has ID Document'
    
    actions = ['approve_applications', 'reject_applications', 'approve_documents', 'reject_documents']
    
    def approve_applications(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(status='pending').update(
            status='approved',
            approved_by=request.user,
            approved_at=timezone.now()
        )
        self.message_user(request, f'{updated} applications approved successfully.')
    approve_applications.short_description = 'Approve selected applications'
    
    def reject_applications(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f'{updated} applications rejected successfully.')
    reject_applications.short_description = 'Reject selected applications'
    
    def approve_documents(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(identity_document_status='pending').update(
            identity_document_status='approved',
            documents_reviewed_by=request.user,
            documents_reviewed_at=timezone.now()
        )
        self.message_user(request, f'{updated} document sets approved successfully.')
    approve_documents.short_description = 'Approve selected documents'
    
    def reject_documents(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(identity_document_status='pending').update(
            identity_document_status='rejected',
            documents_reviewed_by=request.user,
            documents_reviewed_at=timezone.now()
        )
        self.message_user(request, f'{updated} document sets rejected successfully.')
    reject_documents.short_description = 'Reject selected documents (require resubmission)'
    
    fieldsets = (
        ('Application Info', {
            'fields': ('user', 'application_type', 'status', 'amount')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'middle_name', 'last_name', 'email', 'phone', 'date_of_birth')
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'state', 'zip_code', 'country')
        }),
        ('Family Information', {
            'fields': ('spouse_name', 'spouse_phone', 'child_1', 'child_2', 'child_3', 'child_4', 'child_5')
        }),
        ('Parents Information', {
            'fields': ('parent_1', 'parent_2', 'spouse_parent_1', 'spouse_parent_2')
        }),
        ('Siblings & Representative', {
            'fields': ('sibling_1', 'sibling_2', 'sibling_3', 'authorized_rep')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship')
        }),
        ('Employment Information', {
            'fields': ('occupation', 'employer', 'annual_income')
        }),
        ('Document Uploads', {
            'fields': ('identity_document', 'supporting_document_1', 'supporting_document_2', 'supporting_document_3'),
            'classes': ('collapse',)
        }),
        ('Document Review', {
            'fields': ('identity_document_status', 'documents_review_notes', 'documents_reviewed_by', 'documents_reviewed_at'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('notes', 'admin_notes', 'constitution_agreed')
        }),
        ('Approval Information', {
            'fields': ('approved_at', 'approved_by', 'rejection_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        from django.utils import timezone
        if change:
            # Handle application approval
            if obj.status == 'approved' and not obj.approved_by:
                obj.approved_by = request.user
                obj.approved_at = timezone.now()
            
            # Handle document review
            if 'identity_document_status' in form.changed_data and not obj.documents_reviewed_by:
                obj.documents_reviewed_by = request.user
                obj.documents_reviewed_at = timezone.now()
        
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'approved_by')