"""
validators/email_validator.py

Enterprise Email Validation Layer
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from email_validator import (
    validate_email,
    EmailNotValidError,
)


@dataclass
class EmailValidationResult:

    valid: bool

    email: str

    normalized: Optional[str]

    domain: Optional[str]

    reason: Optional[str]


class EmailValidator:
    """
    Enterprise email validation service.

    Responsibilities:
    - validate email syntax
    - validate domain structure
    - normalize email
    - return structured result
    """

    @classmethod
    def validate(
        cls,
        email: str,
    ) -> EmailValidationResult:

        try:

            result = validate_email(
                email,
                check_deliverability=False,
            )

            normalized = (
                result.normalized
            )

            domain = (
                normalized.split("@")[1]
            )

            return EmailValidationResult(
                valid=True,
                email=email,
                normalized=normalized,
                domain=domain,
                reason=None,
            )

        except EmailNotValidError as e:

            return EmailValidationResult(
                valid=False,
                email=email,
                normalized=None,
                domain=None,
                reason=str(e),
            )

    @classmethod
    def validate_many(
        cls,
        emails: List[str],
    ) -> List[EmailValidationResult]:

        results = []

        for email in emails:

            results.append(
                cls.validate(email)
            )

        return results