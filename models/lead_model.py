"""
models/lead_model.py

Root Lead Entity

Acts as the central data contract
between extraction, storage,
AI enrichment and exports.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from uuid import uuid4

# pyrefly: ignore [missing-import]
from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


from models.contact_model import (
    ContactModel
)

from models.company_model import (
    CompanyModel
)

from models.address_model import (
    AddressModel
)    

class LeadModel(BaseModel):

    # ---------------------------------
    # Identity
    # ---------------------------------

    lead_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    source_url: Optional[str] = None

    # ---------------------------------
    # Company
    # ---------------------------------

    # company_name: Optional[str] = None

    # website: Optional[str] = None

    # title: Optional[str] = None

    # ---------------------------------
    # Contacts
    # ---------------------------------

    # emails: List[str] = Field(
    #     default_factory=list
    # )

    # phones: List[str] = Field(
    #     default_factory=list
    # )

    # linkedin_urls: List[str] = Field(
    #     default_factory=list
    # )

    # ---------------------------------
    # Address
    # ---------------------------------

    # address: Optional[str] = None

    # city: Optional[str] = None

    # state: Optional[str] = None

    # country: Optional[str] = None

    contact: ContactModel = Field(
        default_factory=ContactModel
    )

    company: CompanyModel = Field(
        default_factory=CompanyModel
    )

    address: AddressModel = Field(
        default_factory=AddressModel
    )

    # ---------------------------------
    # Metadata
    # ---------------------------------

    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )

    extracted_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    scraper_version: str = "1.0.0"

    # ---------------------------------
    # Pydantic Config
    # ---------------------------------

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        validate_assignment=True,
    )

    # ---------------------------------
    # Export Helpers
    # ---------------------------------

    def to_dict(self) -> Dict[str, Any]:

        return self.model_dump()

    def to_json(self) -> str:

        return self.model_dump_json(
            indent=2
        )

    def to_sheet_row(self) -> Dict[str, str]:

        return {

            "lead_id":
                self.lead_id,

            "company_name":
                self.company_name or "",

            "emails":
                ", ".join(self.emails),

            "phones":
                ", ".join(self.phones),

            "linkedin_urls":
                ", ".join(
                    self.linkedin_urls
                ),

            "website":
                self.website or "",

            "address":
                self.address or "",

            "source_url":
                self.source_url or "",
        }

    # ---------------------------------
    # Business Helpers
    # ---------------------------------

    @property
    def has_contact_data(
        self,
    ) -> bool:

        return bool(

            self.emails
            or self.phones
            or self.linkedin_urls

        )

    @property
    def lead_score(
        self,
    ) -> int:

        score = 0

        if self.emails:
            score += 30

        if self.phones:
            score += 30

        if self.linkedin_urls:
            score += 20

        if self.website:
            score += 10

        if self.address:
            score += 10

        return score