import os
import json
import asyncio
import logging
import google.generativeai as genai

from models.ai_request import AIRequest
from models.ai_result_model import AIResult
from services.providers.base_provider import BaseAIProvider

logger = logging.getLogger(__name__)

class GeminiProvider(BaseAIProvider):
    MAX_RETRIES = 3
    MODEL_NAME = "gemini-2.5-flash"

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            # We don't want to crash on init if they just want to run other parts
            # But the user diff throws ValueError.
            raise ValueError("GEMINI_API_KEY not found")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(self.MODEL_NAME)

    async def extract(self, request: AIRequest) -> AIResult:
        prompt = self._build_prompt(request)
        for attempt in range(self.MAX_RETRIES):
            try:
                response = self.model.generate_content(prompt)
                data = self._parse_response(response.text)
                return AIResult(
                    company_name=data.get("company_name"),
                    ceo_name=data.get("ceo_name"),
                    founder_name=data.get("founder_name"),
                    industry=data.get("industry"),
                    description=data.get("description"),
                    address=data.get("address"),
                    confidence=float(data.get("confidence", 0.0)),
                )
            except Exception as exc:
                logger.exception("Gemini extraction failed")
                if attempt == self.MAX_RETRIES - 1:
                    raise
                await asyncio.sleep(2 ** attempt)
        return AIResult()

    def _build_prompt(self, request: AIRequest) -> str:
        fields = request.requested_fields if request.requested_fields else [
            "company_name", "industry", "description", "address", "ceo_name", "founder_name"
        ]
        json_schema = {field: None for field in fields}
        json_schema["confidence"] = 0.0
        return f"""
You are a lead enrichment engine.
Rules:
1. Extract ONLY factual data.
2. If information is not found return null.
3. Do NOT hallucinate.
4. Return valid JSON only.
5. No markdown.
6. No explanation.

JSON FORMAT:
{json.dumps(json_schema, indent=2)}

PAGE DATA:
{request.build_context()}
"""

    def _parse_response(self, response_text: str) -> dict:
        cleaned = response_text.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned)
