from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payer_name', 'amount', 'payment_method', 'status', 'created_at', 'user')
    list_filter = ('payment_method', 'status', 'currency', 'created_at')
    search_fields = ('payer_name', 'payer_email', 'transaction_id', 'paypal_order_id', 'stripe_payment_intent_id')
    readonly_fields = ('created_at', 'updated_at', 'completed_at')
    
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