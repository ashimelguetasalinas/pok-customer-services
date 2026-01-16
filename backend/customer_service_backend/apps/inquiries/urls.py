from django.urls import path
from .views import (
    InquiryCreateView,
    InquiryListView,
    InquiryDetailView,
)

urlpatterns = [
    path("", InquiryListView.as_view(), name="inquiry-list"),
    path("create/", InquiryCreateView.as_view(), name="inquiry-create"),
    path("<int:pk>/", InquiryDetailView.as_view(), name="inquiry-detail"),
]
