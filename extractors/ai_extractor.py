"""
extractors/ai_extractor.py

AI Extraction Layer

Responsibilities:
- receive DOM output
- build AIRequest
- call AIService
- return AIResult

Does NOT:
- call Gemini directly
- manage API keys
- parse AI JSON
- handle retries
"""

from typing import Dict
from urllib.parse import urlparse

from services.ai_service import (
    AIService
)

from models.ai_request import (
    AIRequest
)

from models.ai_result_model import (
    AIResult
)

from utils.logger import logger


class AIExtractor:

    def __init__(self):

        self.ai_service = (
            AIService()
        )

        logger.info(
            "AIExtractor initialized"
        )

    async def extract(
        self,
        url: str,
        dom_data: Dict,
        requested_fields: list[str],
    ) -> AIResult:

        logger.info(
            "Starting AI extraction"
        )

        request = (
            self._build_request(
                url=url,
                dom_data=dom_data,
                requested_fields=requested_fields,
            )
        )

        result = await (
            self.ai_service.extract(
                request
            )
        )

        logger.info(
            "AI extraction completed"
        )

        return result

    def _build_request(
        self,
        url: str,
        dom_data: Dict,
        requested_fields: list[str],
    ) -> AIRequest:

        parsed = (
            urlparse(url)
        )

        return AIRequest(

            url=url,

            source_domain=
            parsed.netloc,

            title=
            dom_data.get(
                "title"
            ),

            meta_description=
            dom_data.get(
                "meta"
            ),

            visible_text=
            dom_data.get(
                "visible_text"
            ),

            schema_data=
            dom_data.get(
                "schema"
            ),

            open_graph_data=
            dom_data.get(
                "open_graph"
            ),

            requested_fields=
            requested_fields,
        )