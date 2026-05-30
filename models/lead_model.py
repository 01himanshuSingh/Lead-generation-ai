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
            self.company.name or "",

        "emails":
            ", ".join(
                self.contact.emails
            ),

        "phones":
            ", ".join(
                self.contact.phones
            ),

        "linkedin_urls":
            ", ".join(
                self.contact.linkedin_urls
            ),

        "website":
            self.company.website or "",

        "address":
            self.address.full_address or "",

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

            self.contact.emails
            or self.contact.phones
            or self.contact.linkedin_urls

        )

    @property
    def lead_score(
        self,
    ) -> int:

        score = 0

        if self.contact.emails:
            score += 30

        if self.contact.phones:
            score += 30

        if self.contact.linkedin_urls:
            score += 20

        if self.company.website:
            score += 10

        if self.address.full_address:
            score += 10

        return score

    def log(self):
    
        print("\n========== LEAD ==========")
    
        print(f"Lead ID      : {self.lead_id}")
        print(f"Source URL   : {self.source_url}")
    
        print("\n--- Contact ---")
    
        print(f"Emails       : {self.contact.emails}")
        print(f"Phones       : {self.contact.phones}")
        print(f"LinkedIn     : {self.contact.linkedin_urls}")
        print(f"Websites     : {self.contact.websites}")
    
        print("\n--- Company ---")
    
        print(f"Name         : {self.company.name}")
        print(f"Website      : {self.company.website}")
        print(f"Industry     : {self.company.industry}")
        print(f"Description  : {self.company.description}")
    
        print("\n--- Address ---")
    
        print(f"Address      : {self.address.full_address}")
        print(f"City         : {self.address.city}")
        print(f"State        : {self.address.state}")
        print(f"Country      : {self.address.country}")
    
        print("\n--- Metadata ---")
    
        for k, v in self.metadata.items():
    
            print(f"{k:12}: {v}")
    
        print("\n==========================\n")