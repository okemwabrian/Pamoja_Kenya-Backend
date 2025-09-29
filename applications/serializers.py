from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at', 'approved_at', 'approved_by')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            'application_type', 'first_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'address', 'city', 'state', 'zip_code', 'country',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship',
            'occupation', 'employer', 'annual_income', 'amount', 'notes'
        )

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)