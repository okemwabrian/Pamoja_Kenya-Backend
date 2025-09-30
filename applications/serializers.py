from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    identity_document_status_display = serializers.CharField(source='get_identity_document_status_display', read_only=True)
    
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = (
            'user', 'created_at', 'updated_at', 'approved_at', 'approved_by',
            'documents_reviewed_by', 'documents_reviewed_at', 'identity_document_status'
        )

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            'application_type', 'first_name', 'middle_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'address', 'city', 'state', 'zip_code', 'country',
            'spouse_name', 'spouse_phone', 'child_1', 'child_2', 'child_3', 'child_4', 'child_5',
            'parent_1', 'parent_2', 'spouse_parent_1', 'spouse_parent_2',
            'sibling_1', 'sibling_2', 'sibling_3', 'authorized_rep',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship',
            'occupation', 'employer', 'annual_income', 'amount', 'notes',
            'identity_document', 'supporting_document_1', 'supporting_document_2', 'supporting_document_3',
            'constitution_agreed'
        )

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)