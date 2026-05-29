"""
utils/url_normalizer.py

Enterprise URL Normalization Layer
"""

from __future__ import annotations

from urllib.parse import (
    urlparse,
    urlunparse,
)

from typing import List


class URLNormalizer:
    """
    Enterprise URL normalization service.

    Responsibilities:
    - normalize URLs
    - add protocol
    - remove tracking params
    - normalize domains
    - deduplicate URLs
    """

    TRACKING_PARAMS = {

        "utm_source",
        "utm_medium",
        "utm_campaign",
        "utm_term",
        "utm_content",
        "fbclid",
        "gclid",
    }

    @classmethod
    def normalize(
        cls,
        url: str,
    ) -> str | None:

        if not url:
            return None

        url = url.strip()

        # Add protocol
        if not url.startswith(
            ("http://", "https://")
        ):
            url = f"https://{url}"

        parsed = urlparse(url)

        # Lowercase domain
        netloc = parsed.netloc.lower()

        # Remove query params
        clean_query = ""

        # Remove fragment
        fragment = ""

        normalized = urlunparse(
            (
                "https",
                netloc,
                parsed.path.rstrip("/"),
                "",
                clean_query,
                fragment,
            )
        )

        return normalized

    @classmethod
    def normalize_many(
        cls,
        urls: List[str],
    ) -> List[str]:

        normalized = set()

        for url in urls:

            value = cls.normalize(
                url
            )

            if value:
                normalized.add(value)

        return sorted(
            normalized
        )