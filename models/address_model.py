"""
models/address_model.py

Address Entity

Responsible for:
- address information
- geo information
- location normalization

Reusable across:
- LeadModel
- CompanyModel
- AI Enrichment
- CRM Systems
"""

from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Dict,
    Any,
    Optional,
)


@dataclass(slots=True)
class AddressModel:

    # ---------------------------------
    # Address Components
    # ---------------------------------

    full_address: Optional[str] = None

    address_line_1: Optional[str] = None

    address_line_2: Optional[str] = None

    city: Optional[str] = None

    state: Optional[str] = None

    postal_code: Optional[str] = None

    country: Optional[str] = None

    # ---------------------------------
    # Geo Information
    # ---------------------------------

    latitude: Optional[float] = None

    longitude: Optional[float] = None

    # ---------------------------------
    # Metadata
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

            "full_address":
                self.full_address,

            "address_line_1":
                self.address_line_1,

            "address_line_2":
                self.address_line_2,

            "city":
                self.city,

            "state":
                self.state,

            "postal_code":
                self.postal_code,

            "country":
                self.country,

            "latitude":
                self.latitude,

            "longitude":
                self.longitude,

            "confidence_score":
                self.confidence_score,

            "metadata":
                self.metadata,
        }

    # ---------------------------------
    # Business Rules
    # ---------------------------------

    @property
    def is_complete(
        self,
    ) -> bool:

        return bool(

            self.full_address
            and self.city
            and self.state
            and self.country

        )

    @property
    def has_geo_coordinates(
        self,
    ) -> bool:

        return (
            self.latitude is not None
            and self.longitude is not None
        )

    @property
    def address_score(
        self,
    ) -> int:

        score = 0

        if self.full_address:
            score += 30

        if self.city:
            score += 20

        if self.state:
            score += 20

        if self.country:
            score += 20

        if self.postal_code:
            score += 10

        return score

    # ---------------------------------
    # Merge Support
    # ---------------------------------

    def merge(
        self,
        other: "AddressModel",
    ) -> None:

        if not self.full_address:
            self.full_address = other.full_address

        if not self.address_line_1:
            self.address_line_1 = other.address_line_1

        if not self.address_line_2:
            self.address_line_2 = other.address_line_2

        if not self.city:
            self.city = other.city

        if not self.state:
            self.state = other.state

        if not self.postal_code:
            self.postal_code = other.postal_code

        if not self.country:
            self.country = other.country

        if self.latitude is None and other.latitude is not None:
            self.latitude = other.latitude

        if self.longitude is None and other.longitude is not None:
            self.longitude = other.longitude

        self.metadata.update(
            other.metadata
        )