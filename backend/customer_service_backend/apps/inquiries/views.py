from rest_framework import generics, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema


from .models import Inquiry
from .serializers import (
    InquiryCreateSerializer,
    InquiryListSerializer,
    InquiryDetailSerializer,
    InquiryCreatedResponseSerializer,
)
from .tasks import process_inquiry_ai

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


class InquiryDetailView(generics.RetrieveAPIView):
    queryset = Inquiry.objects.all()
    serializer_class = InquiryDetailSerializer
