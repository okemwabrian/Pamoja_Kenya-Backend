from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirm', 'phone')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    identifier = serializers.CharField(required=False)
    password = serializers.CharField()

    def validate(self, attrs):
        identifier = attrs.get('identifier') or attrs.get('username') or attrs.get('email')
        password = attrs.get('password')

        if not identifier or not password:
            raise serializers.ValidationError('Must include username/email and password')
            
        # Since USERNAME_FIELD is 'email', authenticate with email directly
        user = authenticate(username=identifier, password=password)
        
        # If that fails and identifier doesn't contain @, try to find user by username and auth with email
        if not user and '@' not in identifier:
            try:
                user_obj = User.objects.get(username=identifier)
                user = authenticate(username=user_obj.email, password=password)
            except User.DoesNotExist:
                pass

        if not user:
            raise serializers.ValidationError('Invalid credentials')
        
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled')

        attrs['user'] = user
        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 
                 'phone', 'address', 'city', 'state', 'zip_code', 'membership_status',
                 'is_active', 'created_at')
        read_only_fields = ('id', 'created_at')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                 'phone', 'address', 'city', 'state', 'zip_code', 'membership_status')
        read_only_fields = ('id', 'username', 'membership_status')