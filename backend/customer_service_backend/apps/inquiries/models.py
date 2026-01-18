from django.db import models

class Inquiry(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processed", "Processed"),
        ("failed", "Failed"),
        ("finished", "Finished"),
    ]

    CATEGORY_CHOICES = (
        ("sales", "Sales"),
        ("technical_support", "Technical Support"),
        ("complaint", "Complaint"),
        ("spam", "Spam"),
        ("billing", "Billing"),
        ("general_inquiry", "General Inquiry"),
    )

    SENTIMENT_CHOICES = (
        ("positive", "Positive"),
        ("neutral", "Neutral"),
        ("negative", "Negative"),
    )

    customer_name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=True, db_index=True)
    sentiment = models.CharField(max_length=50, choices=SENTIMENT_CHOICES, null=True, db_index=True)
    suggested_response = models.TextField(null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.customer_name} - {self.status}"
