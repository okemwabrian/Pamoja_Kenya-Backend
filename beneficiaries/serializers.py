from rest_framework import serializers
from .models import Beneficiary, BeneficiaryChangeRequest

class BeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class BeneficiaryChangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeneficiaryChangeRequest
        fields = '__all__'
        read_only_fields = ('user', 'status', 'admin_notes', 'created_at', 'updated_at', 
                           'processed_at', 'processed_by')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)