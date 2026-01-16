from celery import shared_task
from .models import Inquiry
from .services.ai_service import InquiryAIService

@shared_task(bind=True, max_retries=3)
def process_inquiry_ai(self, inquiry_id):
    inquiry = Inquiry.objects.get(id=inquiry_id)

    try:
        ai_service = InquiryAIService()
        result = ai_service.analyze_inquiry(inquiry.message)

        inquiry.category = result["category"]
        inquiry.sentiment = result["sentiment"]
        inquiry.suggested_response = result["suggested_response"]
        inquiry.status = "processed"
        inquiry.save()

    except Exception as exc:
        print("🔥 ERROR EN IA:", exc)   # <-- CLAVE
        inquiry.status = "failed"
        inquiry.save(update_fields=["status"])
        raise self.retry(exc=exc, countdown=10)
