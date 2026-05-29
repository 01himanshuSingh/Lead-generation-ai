"""
models/contact_model.py

Contact Entity

Responsible for:
- emails
- phones
- linkedin profiles
- websites

Reusable across:
- LeadModel
- CompanyModel
- Future CRM integrations
"""

from dataclasses import (
    dataclass,
    field,
)
from typing import List, Dict, Any


@dataclass(slots=True)
class ContactModel:

    # -------------------------
    # Core Contact Data
    # -------------------------

    emails: List[str] = field(
        default_factory=list
    )

    phones: List[str] = field(
        default_factory=list
    )

    linkedin_urls: List[str] = field(
        default_factory=list
    )

    websites: List[str] = field(
        default_factory=list
    )

    # -------------------------
    # Export Helpers
    # -------------------------

    def to_dict(
        self,
    ) -> Dict[str, Any]:

        return {

            "emails":
                self.emails,

            "phones":
                self.phones,

            "linkedin_urls":
                self.linkedin_urls,

            "websites":
                self.websites,
        }

    # -------------------------
    # Business Rules
    # -------------------------

    @property
    def has_email(
        self,
    ) -> bool:

        return len(
            self.emails
        ) > 0

    @property
    def has_phone(
        self,
    ) -> bool:

        return len(
            self.phones
        ) > 0

    @property
    def has_linkedin(
        self,
    ) -> bool:

        return len(
            self.linkedin_urls
        ) > 0

    @property
    def contact_score(
        self,
    ) -> int:

        score = 0

        if self.emails:
            score += 40

        if self.phones:
            score += 30

        if self.linkedin_urls:
            score += 20

        if self.websites:
            score += 10

        return score

    # -------------------------
    # Merge Contacts
    # -------------------------

    def merge(
        self,
        other: "ContactModel",
    ) -> None:

        self.emails = list(
            dict.fromkeys(
                self.emails +
                other.emails
            )
        )

        self.phones = list(
            dict.fromkeys(
                self.phones +
                other.phones
            )
        )

        self.linkedin_urls = list(
            dict.fromkeys(
                self.linkedin_urls +
                other.linkedin_urls
            )
        )

        self.websites = list(
            dict.fromkeys(
                self.websites +
                other.websites
            )
        )