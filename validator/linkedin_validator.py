from dataclasses import dataclass
from typing import List
from urllib.parse import urlparse


@dataclass(slots=True)
class LinkedInValidationResult:

    url: str
    valid: bool
    reason: str | None = None


class LinkedInValidator:

    ALLOWED_PATHS = {
        "in",
        "company",
    }

    @classmethod
    def validate(
        cls,
        url: str,
    ) -> LinkedInValidationResult:

        try:

            parsed = urlparse(url)

            domain = parsed.netloc.lower()

            if "linkedin.com" not in domain:

                return LinkedInValidationResult(
                    url=url,
                    valid=False,
                    reason="invalid_domain",
                )

            path_parts = [

                p for p in parsed.path.split("/")
                if p
            ]

            if not path_parts:

                return LinkedInValidationResult(
                    url=url,
                    valid=False,
                    reason="empty_path",
                )

            if path_parts[0] not in cls.ALLOWED_PATHS:

                return LinkedInValidationResult(
                    url=url,
                    valid=False,
                    reason="unsupported_linkedin_type",
                )

            return LinkedInValidationResult(
                url=url,
                valid=True,
            )

        except Exception:

            return LinkedInValidationResult(
                url=url,
                valid=False,
                reason="validation_error",
            )

    @classmethod
    def validate_many(
        cls,
        urls: List[str],
    ) -> List[LinkedInValidationResult]:

        return [
            cls.validate(url)
            for url in urls
        ]