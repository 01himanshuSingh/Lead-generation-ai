"""
utils/phone_validator.py
"""

from dataclasses import dataclass
from typing import Optional, List

# pyrefly: ignore [missing-import]
import phonenumbers
# pyrefly: ignore [missing-import]
from phonenumbers import (
    NumberParseException,
    PhoneNumberType,
    carrier,
    geocoder,
)


@dataclass
class ValidationResult:

    valid: bool

    normalized: str

    country: Optional[str]

    country_name: Optional[str]

    phone_type: Optional[str]

    reason: Optional[str]


class PhoneValidator:
    """
    Enterprise-grade phone validation layer.

    Responsibilities:
    - validate numbers
    - detect country
    - detect phone type
    - return structured result
    """

    TYPE_MAP = {

        PhoneNumberType.MOBILE:
            "MOBILE",

        PhoneNumberType.FIXED_LINE:
            "LANDLINE",

        PhoneNumberType.FIXED_LINE_OR_MOBILE:
            "LANDLINE_OR_MOBILE",

        PhoneNumberType.TOLL_FREE:
            "TOLL_FREE",

        PhoneNumberType.VOIP:
            "VOIP",
    }

    @classmethod
    def validate(
        cls,
        phone: str,
        default_region: str = "IN",
    ) -> ValidationResult:

        try:

            parsed = phonenumbers.parse(
                phone,
                default_region,
            )

            if not phonenumbers.is_valid_number(
                parsed
            ):

                return ValidationResult(
                    valid=False,
                    normalized=phone,
                    country=None,
                    country_name=None,
                    phone_type=None,
                    reason="Invalid phone number",
                )

            country = (
                phonenumbers.region_code_for_number(
                    parsed
                )
            )

            country_name = (
                geocoder.description_for_number(
                    parsed,
                    "en",
                )
            )

            phone_type = (
                cls.TYPE_MAP.get(
                    phonenumbers.number_type(
                        parsed
                    ),
                    "UNKNOWN",
                )
            )

            normalized = (
                phonenumbers.format_number(
                    parsed,
                    phonenumbers.PhoneNumberFormat.E164,
                )
            )

            return ValidationResult(
                valid=True,
                normalized=normalized,
                country=country,
                country_name=country_name,
                phone_type=phone_type,
                reason=None,
            )

        except NumberParseException:

            return ValidationResult(
                valid=False,
                normalized=phone,
                country=None,
                country_name=None,
                phone_type=None,
                reason="Parse failed",
            )

    @classmethod
    def validate_many(
        cls,
        phones: List[str],
        default_region: str = "IN",
    ) -> List[ValidationResult]:

        return [
            cls.validate(phone, default_region)
            for phone in phones
        ]