from dataclasses import dataclass
from typing import List
from urllib.parse import urlparse


@dataclass(slots=True)
class LinkedInRecord:

    original: str
    normalized: str


class LinkedInNormalizer:

    @classmethod
    def normalize(
        cls,
        url: str,
    ) -> LinkedInRecord:

        url = url.strip()

        # Remove tracking params
        url = url.split("?")[0]

        # Remove fragments
        url = url.split("#")[0]

        # Remove trailing slash
        url = url.rstrip("/")

        parsed = urlparse(url)

        normalized = (
            f"{parsed.scheme}://"
            f"{parsed.netloc.lower()}"
            f"{parsed.path}"
        )

        return LinkedInRecord(
            original=url,
            normalized=normalized,
        )

    @classmethod
    def normalize_many(
        cls,
        urls: List[str],
    ) -> List[str]:

        seen = set()

        results = []

        for url in urls:

            record = cls.normalize(url)

            if record.normalized in seen:
                continue

            seen.add(record.normalized)

            results.append(
                record.normalized
            )

        return results