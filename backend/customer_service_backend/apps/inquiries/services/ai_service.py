import json
import os
from openai import OpenAI, OpenAIError

# =========================
# ENUMS CONTROLADOS
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

# =========================
# PROMPTS
# =========================
SYSTEM_PROMPT = """
You are an internal AI classification engine for a customer service platform.
You do NOT chat with users.
You ONLY return valid JSON.

Classification rules:
- If the message is irrelevant, promotional, automated, or malicious,
  classify it as "spam" and set sentiment to "neutral".
- Spam messages MUST always have sentiment = "neutral".
- Do NOT invent information.
- Base the classification strictly on the message content.

Output rules:
- Output MUST be valid JSON
- Do NOT include explanations
- Do NOT include markdown
- Do NOT include additional fields
- Values must strictly follow the allowed enums
"""

USER_PROMPT_TEMPLATE = """
Analyze the following customer message and return a JSON object with:

Fields:
- category: One of ["sales", "technical_support", "billing", "complaint", "spam", "general_inquiry"]
- sentiment: One of ["positive", "neutral", "negative"]
- suggested_response: A short, professional response that a customer service agent could send.

Customer message:
\"\"\"{message}\"\"\"
"""

# =========================
# SERVICIO IA
# =========================
class InquiryAIService:
    """
    Servicio responsable de interactuar con OpenAI y
    devolver una respuesta estructurada y validada.
    """

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable is not set")

        self.client = OpenAI(api_key=api_key)

    def analyze_inquiry(self, message: str) -> dict:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": USER_PROMPT_TEMPLATE.format(message=message)},
                ],
                temperature=0.2,
            )

            content = response.choices[0].message.content
            parsed = json.loads(content)

            self._validate_response(parsed)
            return parsed

        except (json.JSONDecodeError, KeyError, ValueError) as exc:
            raise RuntimeError(f"Invalid AI response format: {exc}")

        except OpenAIError as exc:
            raise RuntimeError(f"OpenAI API error: {exc}")

    # =========================
    # VALIDACIÓN DURA
    # =========================
    def _validate_response(self, data: dict):
        if not isinstance(data, dict):
            raise ValueError("AI response is not a JSON object")

        category = data.get("category")
        sentiment = data.get("sentiment")

        if category not in CATEGORIES:
            raise ValueError("Invalid category")

        if sentiment not in SENTIMENTS:
            raise ValueError("Invalid sentiment")

        if not data.get("suggested_response"):
            raise ValueError("Missing suggested_response")

        # Regla dura de negocio
        if category == "spam" and sentiment != "neutral":
            raise ValueError("Spam messages must have neutral sentiment")

