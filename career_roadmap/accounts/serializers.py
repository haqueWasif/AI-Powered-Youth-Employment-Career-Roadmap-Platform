from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Profile

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 
                  'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)

class ProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            'id',
            'user_email',
            'user_name',
            'education_level',
            'department',
            'experience_level',
            'career_track',
            'skills',
            'experience_description',
            'cv_text',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_skills(self, value):
        """Ensure skills is a list"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Skills must be a list")
        return value


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Simplified serializer for profile updates"""
    
    class Meta:
        model = Profile
        fields = [
            'education_level',
            'department',
            'experience_level',
            'career_track',
            'skills',
            'experience_description',
            'cv_text'
        ]