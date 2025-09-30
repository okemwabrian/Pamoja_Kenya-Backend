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
    email = serializers.EmailField(required=False)
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        
        identifier = username or email
        if not identifier or not password:
            raise serializers.ValidationError('Username/email and password are required')
        
        # Since USERNAME_FIELD = 'email', we need to get the email for authentication
        auth_email = email
        if username and not email:
            try:
                user_obj = User.objects.get(username=username)
                auth_email = user_obj.email
            except User.DoesNotExist:
                raise serializers.ValidationError('Invalid credentials')
        
        user = authenticate(username=auth_email, password=password)

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
                 'is_active', 'is_staff', 'is_superuser', 'created_at')
        read_only_fields = ('id', 'created_at')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                 'phone', 'address', 'city', 'state', 'zip_code', 'membership_status')
        read_only_fields = ('id', 'username', 'membership_status')