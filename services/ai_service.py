from models.ai_request import AIRequest
from models.ai_result_model import (
    AIResult
)

from services.providers.gemini_provider import (
    GeminiProvider
)


class AIService:

    def __init__(self):

        self.provider = (
            GeminiProvider()
        )

    async def extract(
        self,
        request: AIRequest,
    ) -> AIResult:

        return await (
            self.provider.extract(
                request
            )
        )
