from django.urls import path, include

urlpatterns = [
    path("api/inquiries/", include("apps.inquiries.urls")),
]
