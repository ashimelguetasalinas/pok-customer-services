from rest_framework import generics, status, filters, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class IsAdminOrSupport(permissions.BasePermission):
    """
    Permission class to verify if user belongs to Admin or Support groups.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return (
            request.user.is_superuser or 
            request.user.groups.filter(name__in=['Admin', 'Support']).exists()
        )


from .models import Inquiry
from .serializers import (
    InquiryCreateSerializer,
    InquiryListSerializer,
    InquiryDetailSerializer,
    InquiryCreatedResponseSerializer,
)
from .tasks import process_inquiry_ai
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class InquiryCreateView(generics.CreateAPIView):
    queryset = Inquiry.objects.all()
    serializer_class = InquiryCreateSerializer

    @extend_schema(
        request=InquiryCreateSerializer,
        responses={201: InquiryCreateSerializer},
        description="Create an inquiry and send it to AI processing"
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        inquiry = serializer.save(status="pending")
        process_inquiry_ai.delay(inquiry.id)

        return Response(
            InquiryCreatedResponseSerializer(inquiry).data,
            status=status.HTTP_201_CREATED
        )


class InquiryListView(generics.ListAPIView):
    queryset = Inquiry.objects.all().order_by("-created_at")
    serializer_class = InquiryListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'sentiment', 'status']
    search_fields = ['customer_name', 'email', 'message']


class InquiryDetailView(generics.RetrieveUpdateAPIView):
    queryset = Inquiry.objects.all()
    serializer_class = InquiryDetailSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsAdminOrSupport()]
        return [AllowAny()]

    def perform_update(self, serializer):
        user = self.request.user
        validated_data = serializer.validated_data
        instance = serializer.instance

        is_admin = user.is_superuser or user.groups.filter(name='Admin').exists()

        if not is_admin:
            # If not admin, must be support (due to IsAdminOrSupport check)
            # Support can ONLY change category
            if 'status' in validated_data and validated_data['status'] != instance.status:
                raise PermissionDenied("Support roles cannot change inquiry status.")
            
        serializer.save()
