from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CandidateProfile,RecruiterProfile
from django.contrib.auth.models import Group
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """serializers for user registrataion"""
    password = serializers.CharField(write_only=True,min_length=8)
    password_confirm = serializers.CharField(write_only=True,min_length=8)

    class Meta:
        model = User
        fields = ['email','first_name','last_name','password','password_confirm']

    def validate_email(self,value):
        email = value.lower().strip()

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email is already in use")
        
        return email

    def validate(self,attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self,validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            password=password, 
            **validated_data
            )
        
        candidate_group, _ = Group.objects.get_or_create(
            name="Candidate"
            )
        user.groups.add(candidate_group)

        CandidateProfile.objects.create(user=user)
        return user

class UserSerializer(serializers.ModelSerializer):
    """serializer for user model"""
    class Meta:
        model = User
        fields = ['id','email','first_name','last_name','is_active','date_joined']

        read_only_fields = ['id','email','is_active','date_joined']

class LogoutSerializer(serializers.ModelSerializer):
    """serializer for logout view"""
    refresh = serializers.CharField()
    def validate(self,attrs):
        self.token = RefreshToken(attrs['refresh'])
        return attrs

    def save(self, **kwargs):
        try:
            self.token.blacklist()
        except AttributeError:
            self.fail('bad_token')

class CandidateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProfile
        fields = [
            "profile_image",
            "phone",
            "headline",
            "bio",
            "skills",
            "experience",
            "education",
            "resume",
            "portfolio_url",
            "linkedin_url",
            "github_url",
            "created_at",
            "updated_at"
        ]
        read_only_fields = [
            "created_at",
            "updated_at",
        ]


class RecruiterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruiterProfile
        fields = [
            "profile_image",
            "job_title",
            "bio",
            "phone",
            "is_varified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "is_varified",
            "created_at",
            "updated_at"
        ]

