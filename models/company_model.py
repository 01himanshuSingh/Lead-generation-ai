"""
models/company_model.py

Company Entity

Responsible for:
- company information
- business classification
- enrichment metadata

Reusable across:
- LeadModel
- AI Extractor
- CRM Export
"""

from dataclasses import (
    dataclass,
    field,
)
from typing import Dict, Any, Optional


@dataclass(slots=True)
class CompanyModel:

    # ---------------------------------
    # Identity
    # ---------------------------------

    name: Optional[str] = None

    website: Optional[str] = None

    domain: Optional[str] = None

    # ---------------------------------
    # Business Details
    # ---------------------------------

    industry: Optional[str] = None

    description: Optional[str] = None

    category: Optional[str] = None

    company_size: Optional[str] = None

    founded_year: Optional[int] = None

    # ---------------------------------
    # Enrichment
    # ---------------------------------

    confidence_score: float = 0.0

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    # ---------------------------------
    # Export Helpers
    # ---------------------------------

    def to_dict(
        self,
    ) -> Dict[str, Any]:

        return {

            "name":
                self.name,

            "website":
                self.website,

            "domain":
                self.domain,

            "industry":
                self.industry,

            "description":
                self.description,

            "category":
                self.category,

            "company_size":
                self.company_size,

            "founded_year":
                self.founded_year,

            "confidence_score":
                self.confidence_score,

            "metadata":
                self.metadata,
        }

    # ---------------------------------
    # Business Rules
    # ---------------------------------

    @property
    def is_enriched(
        self,
    ) -> bool:

        return bool(

            self.industry
            or self.description
            or self.category

        )

    @property
    def completeness_score(
        self,
    ) -> int:

        score = 0

        if self.name:
            score += 30

        if self.website:
            score += 20

        if self.industry:
            score += 20

        if self.description:
            score += 20

        if self.company_size:
            score += 10

        return score

    # ---------------------------------
    # Merge Support
    # ---------------------------------

    def merge(
        self,
        other: "CompanyModel",
    ) -> None:

        if not self.name:
            self.name = other.name

        if not self.website:
            self.website = other.website

        if not self.domain:
            self.domain = other.domain

        if not self.industry:
            self.industry = other.industry

        if not self.description:
            self.description = other.description

        if not self.category:
            self.category = other.category

        if not self.company_size:
            self.company_size = other.company_size

        if not self.founded_year:
            self.founded_year = other.founded_year

        self.metadata.update(
            other.metadata
        )