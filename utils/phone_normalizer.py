import re
from typing import List


class PhoneNormalizer:
    """
    Enterprise phone normalization layer.

    Responsibilities:
    - Clean phone numbers
    - Standardize formats
    - Handle country prefixes
    - Remove duplicates
    """

    DEFAULT_COUNTRY_CODE = "+91"

    @classmethod
    def normalize(
        cls,
        phone: str,
    ) -> str | None:

        if not phone:
            return None

        # Remove spaces, brackets, dashes
        cleaned = re.sub(
            r"[^\d+]",
            "",
            phone,
        )

        # +91XXXXXXXXXX
        if cleaned.startswith("+91"):
            return cleaned

        # 91XXXXXXXXXX
        if (
            cleaned.startswith("91")
            and len(cleaned) == 12
        ):
            return f"+{cleaned}"

        # Indian mobile
        if (
            len(cleaned) == 10
            and cleaned[0] in "6789"
        ):
            return (
                f"{cls.DEFAULT_COUNTRY_CODE}"
                f"{cleaned}"
            )

        # Landline or unknown
        return cleaned

    @classmethod
    def normalize_many(
        cls,
        phones: List[str],
    ) -> List[str]:

        normalized = set()

        for phone in phones:

            value = cls.normalize(
                phone
            )

            if value:
                normalized.add(value)

        return sorted(normalized)