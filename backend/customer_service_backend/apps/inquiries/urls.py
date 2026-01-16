from django.urls import path
from .views import (
    InquiryCreateView,
    InquiryListView,
    InquiryDetailView,
)

urlpatterns = [
    path("inquiries/", InquiryListView.as_view(), name="inquiry-list"),
    path("inquiries/create/", InquiryCreateView.as_view(), name="inquiry-create"),
    path("inquiries/<int:pk>/", InquiryDetailView.as_view(), name="inquiry-detail"),
]