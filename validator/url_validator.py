"""
validators/url_validator.py

Enterprise URL Validation Layer
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List

# pyrefly: ignore [missing-import]
import validators
# pyrefly: ignore [missing-import]
import tldextract


@dataclass
class URLValidationResult:

    valid: bool

    url: str

    domain: Optional[str]

    subdomain: Optional[str]

    suffix: Optional[str]

    is_social: bool

    reason: Optional[str]


class URLValidator:
    """
    Enterprise URL validation service.
    """

    SOCIAL_DOMAINS = {

        "linkedin.com",
        "facebook.com",
        "instagram.com",
        "twitter.com",
        "x.com",
        "youtube.com",
        "tiktok.com",
    }

    @classmethod
    def validate(
        cls,
        url: str,
    ) -> URLValidationResult:

        if not url:

            return URLValidationResult(
                valid=False,
                url="",
                domain=None,
                subdomain=None,
                suffix=None,
                is_social=False,
                reason="Empty URL",
            )

        is_valid = validators.url(url)

        if not is_valid:

            return URLValidationResult(
                valid=False,
                url=url,
                domain=None,
                subdomain=None,
                suffix=None,
                is_social=False,
                reason="Invalid URL",
            )

        extracted = tldextract.extract(url)

        full_domain = (
            f"{extracted.domain}."
            f"{extracted.suffix}"
        )

        is_social = (
            full_domain.lower()
            in cls.SOCIAL_DOMAINS
        )

        return URLValidationResult(
            valid=True,
            url=url,
            domain=extracted.domain,
            subdomain=extracted.subdomain,
            suffix=extracted.suffix,
            is_social=is_social,
            reason=None,
        )

    @classmethod
    def validate_many(
        cls,
        urls: List[str],
    ) -> List[URLValidationResult]:

        return [
            cls.validate(url)
            for url in urls
        ]