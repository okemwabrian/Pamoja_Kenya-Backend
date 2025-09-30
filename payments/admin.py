from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payer_name', 'amount', 'get_payment_method_display', 'get_status_display', 'created_at', 'user')
    list_filter = ('payment_method', 'status', 'currency', 'created_at', 'completed_at')
    search_fields = ('payer_name', 'payer_email', 'transaction_id', 'paypal_order_id', 'stripe_payment_intent_id', 'user__username')
    readonly_fields = ('created_at', 'updated_at', 'completed_at')
    date_hierarchy = 'created_at'
    
    actions = ['mark_as_completed', 'mark_as_failed']
    
    def mark_as_completed(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(status='pending').update(
            status='completed',
            completed_at=timezone.now()
        )
        self.message_user(request, f'{updated} payments marked as completed.')
    mark_as_completed.short_description = 'Mark selected payments as completed'
    
    def mark_as_failed(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='failed')
        self.message_user(request, f'{updated} payments marked as failed.')
    mark_as_failed.short_description = 'Mark selected payments as failed'
    
    fieldsets = (
        ('Payment Info', {
            'fields': ('user', 'application', 'amount', 'currency', 'payment_method', 'status')
        }),
        ('Payer Information', {
            'fields': ('payer_name', 'payer_email')
        }),
        ('Transaction Details', {
            'fields': ('paypal_order_id', 'stripe_payment_intent_id', 'transaction_id')
        }),
        ('Additional Information', {
            'fields': ('description', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if change and obj.status == 'completed' and not obj.completed_at:
            from django.utils import timezone
            obj.completed_at = timezone.now()
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'application')