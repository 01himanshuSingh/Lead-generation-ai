from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class AIResult:
    company_name: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    ceo_name: Optional[str] = None
    founder_name: Optional[str] = None
    address: Optional[str] = None
    confidence: float = 0.0

    def to_dict(self):
        # Exclude None values to match expected behavior
        return {k: v for k, v in asdict(self).items() if v is not None}
