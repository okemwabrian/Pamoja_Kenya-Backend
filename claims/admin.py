from django.contrib import admin
from django.utils import timezone
from .models import Claim, Beneficiary, BenefitPayment

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('user', 'claim_type', 'amount_requested', 'amount_approved', 'status', 'created_at')
    list_filter = ('claim_type', 'status', 'created_at')
    search_fields = ('user__username', 'user__email', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Claim Information', {
            'fields': ('user', 'claim_type', 'amount_requested', 'description', 'supporting_documents')
        }),
        ('Status & Approval', {
            'fields': ('status', 'amount_approved', 'admin_notes')
        }),
        ('Review Information', {
            'fields': ('reviewed_by', 'reviewed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if change and obj.status in ['approved', 'rejected'] and not obj.reviewed_by:
            obj.reviewed_by = request.user
            obj.reviewed_at = timezone.now()
        super().save_model(request, obj, form, change)

@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'relationship', 'percentage', 'total_benefits_received', 'is_active')
    list_filter = ('relationship', 'is_primary', 'is_active', 'created_at')
    search_fields = ('name', 'user__username', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'total_benefits_received', 'last_benefit_date')
    
    fieldsets = (
        ('Beneficiary Information', {
            'fields': ('user', 'name', 'relationship', 'percentage', 'is_primary', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Benefit History', {
            'fields': ('total_benefits_received', 'last_benefit_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(BenefitPayment)
class BenefitPaymentAdmin(admin.ModelAdmin):
    list_display = ('beneficiary', 'amount', 'claim', 'payment_method', 'paid_at', 'paid_by')
    list_filter = ('payment_method', 'paid_at')
    search_fields = ('beneficiary__name', 'payment_reference', 'claim__description')
    readonly_fields = ('paid_at',)
    
    def save_model(self, request, obj, form, change):
        if not change:  # New payment
            obj.paid_by = request.user
            # Update beneficiary total
            obj.beneficiary.total_benefits_received += obj.amount
            obj.beneficiary.last_benefit_date = timezone.now()
            obj.beneficiary.save()
        super().save_model(request, obj, form, change)