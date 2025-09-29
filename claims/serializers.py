from rest_framework import serializers
from .models import Claim, Beneficiary, BenefitPayment

class ClaimSerializer(serializers.ModelSerializer):
    claim_type_display = serializers.CharField(source='get_claim_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Claim
        fields = ['id', 'claim_type', 'claim_type_display', 'amount_requested', 
                 'amount_approved', 'description', 'status', 'status_display',
                 'admin_notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'admin_notes', 'created_at', 'updated_at']

class ClaimCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = ['claim_type', 'amount_requested', 'description', 'supporting_documents']

class BeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = ['id', 'name', 'relationship', 'phone', 'email', 'address',
                 'percentage', 'is_primary', 'total_benefits_received', 
                 'last_benefit_date', 'created_at']
        read_only_fields = ['id', 'total_benefits_received', 'last_benefit_date', 'created_at']