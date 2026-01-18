from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from openai import OpenAI, AsyncOpenAI, OpenAIError
import json

app = FastAPI()

# Schemas
class AnalyzeRequest(BaseModel):
    message: str

class AnalyzeResponse(BaseModel):
    category: str
    sentiment: str
    suggested_response: str

# Config & Constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
async_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

CATEGORIES = [
    "sales",
    "technical_support",
    "billing",
    "complaint",
    "spam",
    "general_inquiry",
]

SENTIMENTS = ["positive", "neutral", "negative"]

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

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_inquiry(request: AnalyzeRequest):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")

    try:
        response = await async_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT_TEMPLATE.format(message=request.message)},
            ],
            temperature=0.2,
            response_format={"type": "json_object"}, 
        )

        content = response.choices[0].message.content
        parsed = json.loads(content)

        # Basic Validation
        if parsed.get("category") not in CATEGORIES:
            parsed["category"] = "general_inquiry" # Fallback
        
        if parsed.get("sentiment") not in SENTIMENTS:
            parsed["sentiment"] = "neutral" # Fallback

        return AnalyzeResponse(**parsed)

    except OpenAIError as e:
        print(f"OpenAI Error: {e}")
        raise HTTPException(status_code=503, detail="AI Service provider unavailable")
    except Exception as e:
        print(f"Internal Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/health")
def health():
    return {"status": "ok"}
