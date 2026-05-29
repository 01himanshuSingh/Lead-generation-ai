"""Basic data extraction fallbacks.

Enterprise-grade Regex Extraction Engine.

Purpose:
- Fast raw text extraction
- Dynamic extraction routing
- High-performance parsing
- Structured lead extraction

Supports:
- emails
- phone numbers
- linkedin profiles
- websites
- social links

Architecture:
HTML/Text
    ↓
Dynamic Extraction Engine
    ↓
Compiled Regex Patterns
    ↓
Normalization
    ↓
Deduplication
    ↓
Structured Output
"""

from __future__ import annotations

import re

from dataclasses import dataclass
from typing import Dict, List, Callable

from utils.logger import logger


# =========================================================
# Extraction Result Model
# =========================================================

@dataclass(slots=True)
class ExtractionResult:

    field: str
    values: List[str]
    total: int


# =========================================================
# Regex Extraction Engine
# =========================================================

class RegexExtractor:

    def __init__(self):

        logger.info(
            "RegexExtractor initialized"
        )

        # -------------------------------------------------
        # Precompiled Regex Patterns
        # -------------------------------------------------

        self.patterns = {

            "email":
                re.compile(
                    r"""
                    [a-zA-Z0-9._%+-]+
                    @
                    [a-zA-Z0-9.-]+
                    \.
                    [a-zA-Z]{2,}
                    """,
                    re.VERBOSE
                ),

            "phone":
                re.compile(
                    r"""
                    (?:
                        \+?\d{1,3}
                        [\s\-]?
                    )?
                    \(?\d{3}\)?
                    [\s\-]?
                    \d{3}
                    [\s\-]?
                    \d{4}
                    """,
                    re.VERBOSE
                ),

            "linkedin":
                re.compile(
                    r"""
                    https?://
                    (?:www\.)?
                    linkedin\.com/
                    [^\s"'<>]+
                    """,
                    re.VERBOSE
                ),

            "website":
                re.compile(
                    r"""
                    https?://
                    [^\s"'<>]+
                    """,
                    re.VERBOSE
                ),

            "instagram":
                re.compile(
                    r"""
                    https?://
                    (?:www\.)?
                    instagram\.com/
                    [^\s"'<>]+
                    """,
                    re.VERBOSE
                ),
        }

        # -------------------------------------------------
        # Dynamic Extraction Routing
        # -------------------------------------------------

        self.extractor_map: Dict[
            str,
            Callable
        ] = {

            "email":
                self._extract_emails,

            "phone":
                self._extract_phones,

            "linkedin":
                self._extract_linkedin,

            "website":
                self._extract_websites,

            "instagram":
                self._extract_instagram,
        }

    # =====================================================
    # Main Extraction API
    # =====================================================

    def extract(
        self,
        text: str,
        fields: List[str],
    ) -> Dict[str, ExtractionResult]:

        logger.info(
            f"Starting regex extraction -> {fields}"
        )

        results = {}

        for field in fields:

            extractor = (
                self.extractor_map.get(field)
            )

            if not extractor:

                logger.warning(
                    f"No extractor found -> {field}"
                )

                continue

            try:

                values = extractor(text)

                results[field] = (
                    ExtractionResult(
                        field=field,
                        values=values,
                        total=len(values),
                    )
                )

                logger.info(
                    f"{field} extracted -> "
                    f"{len(values)}"
                )

            except Exception as e:

                logger.error(
                    f"{field} extraction failed -> {e}"
                )

        return results

    # =====================================================
    # Email Extraction
    # =====================================================

    def _extract_emails(
        self,
        text: str,
    ) -> List[str]:

        matches = (
            self.patterns["email"]
            .findall(text)
        )

        return self._clean(matches)

    # =====================================================
    # Phone Extraction
    # =====================================================

    def _extract_phones(
        self,
        text: str,
    ) -> List[str]:

        # ---------------------------------
        # Debug Known Phone
        # ---------------------------------

        search_term = "25750034"

        index = text.find(search_term)

        if index != -1:

            print("\n===== PHONE FOUND =====")

            print(
                text[
                    max(0, index - 200):
                    index + 200
                ]
            )

            print("\n=======================\n")

        else:

            print(
                "25750034 NOT FOUND IN PAGE"
            )

        # ---------------------------------
        # Enterprise Phone Pattern
        # ---------------------------------

        phone_pattern = re.compile(
            r"""
            (?:
                \+?\d{1,4}
                [-\s]?
            )?
            (?:
                \(?\d{2,5}\)?
                [-\s]?
            )?
            \d{3,6}
            (?:[-\s]?\d{2,6})+
            """,
            re.VERBOSE,
        )

        matches = phone_pattern.findall(
            text
        )

        print("\nPHONE REGEX MATCHES:")
        print(matches[:20])

        cleaned = []

        for phone in matches:

            phone = phone.strip()

            digits = re.sub(
                r"\D",
                "",
                phone,
            )

            # Ignore garbage values
            if len(digits) < 7:
                continue

            cleaned.append(phone)

        # Remove duplicates
        cleaned = list(
            dict.fromkeys(cleaned)
        )

        print("\nPHONE CLEANED:")
        print(cleaned)

        return cleaned
   # =====================================================
    # LinkedIn Extraction
    # =====================================================

    def _extract_linkedin(
        self,
        text: str,
    ) -> List[str]:

        matches = (
            self.patterns["linkedin"]
            .findall(text)
        )

        cleaned = []

        for url in matches:

            url = url.strip()

            # Remove tracking params
            url = url.split("?")[0]

            # Remove fragments
            url = url.split("#")[0]

            # Remove trailing slash
            url = url.rstrip("/")

            cleaned.append(url)

        # Deduplicate while preserving order
        cleaned = list(
            dict.fromkeys(cleaned)
        )

        return cleaned
    # =====================================================
    # Website Extraction
    # =====================================================

    def _extract_websites(
        self,
        text: str,
    ) -> List[str]:

        matches = (
            self.patterns["website"]
            .findall(text)
        )

        return self._clean(matches)

    # =====================================================
    # Instagram Extraction
    # =====================================================

    def _extract_instagram(
        self,
        text: str,
    ) -> List[str]:

        matches = (
            self.patterns["instagram"]
            .findall(text)
        )

        return self._clean(matches)

    # =====================================================
    # Cleanup + Deduplication
    # =====================================================

    def _clean(
        self,
        values: List[str],
    ) -> List[str]:

        cleaned = []

        for value in values:

            value = value.strip()

            if value:

                cleaned.append(value)

        return list(set(cleaned))