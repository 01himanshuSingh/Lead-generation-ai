from abc import ABC, abstractmethod
from models.ai_request import AIRequest
from models.ai_result_model import AIResult

class BaseAIProvider(ABC):
    @abstractmethod
    async def extract(self, request: AIRequest) -> AIResult:
        """Provider-independent AI extraction."""
        raise NotImplementedError
