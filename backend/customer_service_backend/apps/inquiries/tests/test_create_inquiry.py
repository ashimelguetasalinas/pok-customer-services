from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch

from apps.inquiries.models import Inquiry


class InquiryCreateAPITest(APITestCase):

    @patch("apps.inquiries.views.process_inquiry_ai.delay")
    def test_create_inquiry_triggers_ai_task(self, mock_delay):
        url = reverse("inquiry-create")

        payload = {
            "customer_name": "Juan Perez",
            "email": "juan@test.cl",
            "message": "I need help with my account"
        }

        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Inquiry.objects.count(), 1)
        inquiry = Inquiry.objects.first()
        self.assertEqual(inquiry.status, "pending")
        mock_delay.assert_called_once_with(inquiry.id)
