from django.urls import reverse
from rest_framework.test import APITestCase
from unittest.mock import patch
from apps.inquiries.models import Inquiry

class InquiryAsyncFlowTest(APITestCase):

    @patch("apps.inquiries.views.process_inquiry_ai.delay")
    @patch("apps.inquiries.services.ai_service.InquiryAIService.analyze_inquiry")
    def test_async_ai_processing(self, mock_analyze, mock_delay):

        mock_analyze.return_value = {
            "category": "spam",
            "sentiment": "neutral",
            "suggested_response": "Thank you for your message."
        }

        response = self.client.post(
            "/api/inquiries/create/",
            {
                "customer_name": "Juan",
                "email": "juan@test.cl",
                "message": "Buy cheap crypto now!!!"
            },
            format="json"
        )

        self.assertEqual(response.status_code, 201)

        inquiry = Inquiry.objects.first()
        self.assertIsNotNone(inquiry)

        # Verifica que la task fue llamada
        mock_delay.assert_called_once_with(inquiry.id)
