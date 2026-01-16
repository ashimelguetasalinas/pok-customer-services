from rest_framework import serializers
from .models import Inquiry

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
