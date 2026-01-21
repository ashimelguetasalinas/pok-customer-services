from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.inquiries.models import Inquiry

class InquiryModelTest(TestCase):

    def setUp(self):
        self.inquiry_data = {
            "customer_name": "Juan Perez",
            "email": "juan@test.com",
            "message": "Hola, necesito ayuda.",
        }

    def test_create_inquiry_success(self):
        inquiry = Inquiry.objects.create(**self.inquiry_data)
        self.assertEqual(inquiry.customer_name, "Juan Perez")
        self.assertEqual(inquiry.status, "pending")
        self.assertIsNotNone(inquiry.created_at)

    def test_str_representation(self):
        inquiry = Inquiry.objects.create(**self.inquiry_data)
        self.assertEqual(str(inquiry), "Juan Perez - pending")

    def test_invalid_email(self):
        self.inquiry_data["email"] = "not-an-email"
        inquiry = Inquiry(**self.inquiry_data)
        with self.assertRaises(ValidationError):
            inquiry.full_clean()

    def test_category_choices_validation(self):
        self.inquiry_data["category"] = "invalid_category"
        inquiry = Inquiry(**self.inquiry_data)
        with self.assertRaises(ValidationError):
            inquiry.full_clean()

    def test_sentiment_choices_validation(self):
        self.inquiry_data["sentiment"] = "invalid_sentiment"
        inquiry = Inquiry(**self.inquiry_data)
        with self.assertRaises(ValidationError):
            inquiry.full_clean()
