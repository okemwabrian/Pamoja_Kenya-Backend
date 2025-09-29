from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at', 'completed_at')

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'application', 'amount', 'currency', 'payment_method',
            'payer_name', 'payer_email', 'paypal_order_id', 
            'stripe_payment_intent_id', 'transaction_id', 'description'
        )

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)