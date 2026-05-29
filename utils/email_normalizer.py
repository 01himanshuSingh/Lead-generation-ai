"""
utils/email_normalizer.py

Enterprise Email Normalization Layer
"""

from __future__ import annotations

import unicodedata
from typing import List, Optional


class EmailNormalizer:
    """
    Scalable email normalization service.

    Responsibilities:
    - trim whitespace
    - remove mailto:
    - lowercase emails
    - normalize unicode
    - deduplicate collections
    """

    MAILTO_PREFIX = "mailto:"

    @classmethod
    def normalize(
        cls,
        email: str,
    ) -> Optional[str]:

        if not email:
            return None

        # Remove surrounding spaces
        email = email.strip()

        # Remove mailto:
        if email.lower().startswith(
            cls.MAILTO_PREFIX
        ):
            email = email[
                len(cls.MAILTO_PREFIX):
            ]

        # Normalize unicode
        email = unicodedata.normalize(
            "NFKC",
            email,
        )

        # Lowercase
        email = email.lower()

        # Remove accidental spaces
        email = email.replace(
            " ",
            "",
        )

        return email

    @classmethod
    def normalize_many(
        cls,
        emails: List[str],
    ) -> List[str]:

        normalized = set()

        for email in emails:

            value = cls.normalize(
                email
            )

            if value:
                normalized.add(value)

        return sorted(
            normalized
        )