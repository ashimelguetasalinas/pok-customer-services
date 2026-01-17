from rest_framework import serializers
from .models import Inquiry

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['groups'] = list(user.groups.values_list('name', flat=True))
        token['is_superuser'] = user.is_superuser

        return token

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

class InquiryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = ("customer_name", "email", "message")

class InquiryCreatedResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = ("id", "status")


class InquiryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = (
            "id",
            "customer_name",
            "email",
            "message",
            "category",
            "sentiment",
            "suggested_response",
            "status",
            "created_at",
        )


class InquiryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = "__all__"
