import requests
import os

# =========================
# ENUMS
# =========================
CATEGORIES = [
    "sales",
    "technical_support",
    "billing",
    "complaint",
    "spam",
    "general_inquiry",
]

SENTIMENTS = [
    "positive",
    "neutral",
    "negative",
]

class InquiryAIService:
    """
    Client for the external AI Service.
    """

    def __init__(self):
        # Service URL from env or default to docker service name
        self.service_url = os.getenv("AI_SERVICE_URL", "http://ai-service:8000")

    def analyze_inquiry(self, message: str) -> dict:
        try:
            response = requests.post(
                f"{self.service_url}/analyze",
                json={"message": message},
                timeout=30 
            )
            
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            raise RuntimeError(f"AI Service Error: {e}")
