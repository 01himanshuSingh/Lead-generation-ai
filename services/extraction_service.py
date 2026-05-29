"""
services/extraction_service.py

Data Quality Layer

Responsibilities:
- normalize extracted data
- validate extracted data
- deduplicate values
- prepare structured lead data
"""

from typing import Dict, Any

from utils.phone_normalizer import PhoneNormalizer
from utils.email_normalizer import EmailNormalizer
from utils.url_normalizer import URLNormalizer

from utils.linkedin_normalizer import (
    LinkedInNormalizer
)

from validator.linkedin_validator import (
    LinkedInValidator
)
from validator.phone_validator import PhoneValidator
from validator.email_validator import EmailValidator
from validator.url_validator import URLValidator

from utils.logger import logger


class ExtractionService:

    @staticmethod
    def _extract_values(data):

        if data is None:
            return []

        # ExtractionResult object
        if hasattr(data, "values"):
            return data.values

        # Already a list
        if isinstance(data, list):
            return data

        return []

    @classmethod
    def process(
        cls,
        extracted_data: Dict[str, Any],
    ) -> Dict[str, Any]:

        result = {}

        # -----------------------------
        # EMAILS
        # -----------------------------

        if "email" in extracted_data:

            raw_emails = cls._extract_values(
                extracted_data["email"]
            )

            emails = EmailNormalizer.normalize_many(
                raw_emails
            )

            emails = [

        item.normalized

                for item in EmailValidator
                .validate_many(emails)

                if item.valid
            ]

            result["email"] = emails
        # -----------------------------
        # PHONES
        # -----------------------------

        if "phone" in extracted_data:

            raw_phones = cls._extract_values(
                extracted_data["phone"]
            )

            phones = PhoneNormalizer.normalize_many(
                raw_phones
            )

            phones = [

                item.normalized

                for item in PhoneValidator
                .validate_many(phones)

                if item.valid
            ]

            result["phone"] = phones
        # -----------------------------
        # URLS
        # -----------------------------

        if "linkedin" in extracted_data:

            raw_linkedin = cls._extract_values(
                extracted_data["linkedin"]
            )

            linkedin_urls = (
                LinkedInNormalizer.normalize_many(
                    raw_linkedin
                )
            )

            linkedin_urls = [

                item.url

                for item in LinkedInValidator
                .validate_many(linkedin_urls)

                if item.valid
            ]

            result["linkedin"] = linkedin_urls

        if "website" in extracted_data:

            raw_urls = cls._extract_values(
                extracted_data["website"]
            )

            urls = URLNormalizer.normalize_many(
                raw_urls
            )

            urls = [

        item.url

        for item in URLValidator
        .validate_many(urls)

        if item.valid
    ]

            result["website"] = urls
        # -----------------------------
        # PASS THROUGH
        # -----------------------------

        for field in [

            "title",
            "meta",
            "schema",
            "open_graph",
            "visible_text",
        ]:

            if field in extracted_data:

                result[field] = (
                    extracted_data[field]
                )

        logger.info(
            "ExtractionService completed"
        )

        return result