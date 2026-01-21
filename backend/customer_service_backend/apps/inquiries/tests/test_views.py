from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User, Group
from apps.inquiries.models import Inquiry

class InquiryViewsTest(APITestCase):

    def setUp(self):
        # Create users
        self.admin_user = User.objects.create_superuser(username="admin", email="admin@test.com", password="password")
        self.support_user = User.objects.create_user(username="support", email="support@test.com", password="password")
        self.regular_user = User.objects.create_user(username="user", email="user@test.com", password="password")

        # Create groups
        self.support_group, _ = Group.objects.get_or_create(name="Support")
        self.admin_group, _ = Group.objects.get_or_create(name="Admin")
        self.support_user.groups.add(self.support_group)
        self.admin_user.groups.add(self.admin_group)

        # Create sample inquiries
        self.inquiry = Inquiry.objects.create(
            customer_name="Customer 1",
            email="c1@test.com",
            message="Message 1",
            status="pending"
        )
        self.inquiry2 = Inquiry.objects.create(
            customer_name="Customer 2",
            email="c2@test.com",
            message="Message 2",
            status="processed",
            category="sales"
        )

    def test_list_inquiries_anyone(self):
        url = reverse("inquiry-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify pagination and count
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 2)

    def test_filter_inquiries_by_category(self):
        url = reverse("inquiry-list")
        response = self.client.get(url, {"category": "sales"})
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["customer_name"], "Customer 2")

    def test_retrieve_inquiry_anyone(self):
        url = reverse("inquiry-detail", kwargs={"pk": self.inquiry.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["customer_name"], "Customer 1")

    def test_update_inquiry_requires_auth(self):
        url = reverse("inquiry-detail", kwargs={"pk": self.inquiry.id})
        response = self.client.patch(url, {"status": "processed"}, format="json")
        # DRF returns 401 if authentication is missing and JWT is default
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_inquiry_admin_success(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("inquiry-detail", kwargs={"pk": self.inquiry.id})
        response = self.client.patch(url, {"status": "processed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.inquiry.refresh_from_db()
        self.assertEqual(self.inquiry.status, "processed")

    def test_update_inquiry_support_restricted(self):
        self.client.force_authenticate(user=self.support_user)
        url = reverse("inquiry-detail", kwargs={"pk": self.inquiry.id})
        
        # Support can change category
        response = self.client.patch(url, {"category": "technical_support"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Support CANNOT change status
        response = self.client.patch(url, {"status": "finished"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        self.inquiry.refresh_from_db()
        self.assertEqual(self.inquiry.status, "pending")
        self.assertEqual(self.inquiry.category, "technical_support")
