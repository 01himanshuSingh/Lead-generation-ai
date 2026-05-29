"""
utils/text_cleaner.py

Enterprise Text Cleaning Layer
"""

from __future__ import annotations

import html
import re
import unicodedata
from typing import List


class TextCleaner:
    """
    Enterprise text cleaning service.

    Responsibilities:
    - normalize unicode
    - clean whitespace
    - remove html entities
    - remove invisible characters
    - prepare text for extraction
    """

    MULTI_SPACE_PATTERN = re.compile(
        r"\s+"
    )

    INVISIBLE_PATTERN = re.compile(
        r"[\u200b-\u200d\uFEFF]"
    )

    @classmethod
    def clean(
        cls,
        text: str,
    ) -> str:

        if not text:
            return ""

        # Decode HTML entities
        text = html.unescape(text)

        # Unicode normalization
        text = unicodedata.normalize(
            "NFKC",
            text,
        )

        # Remove invisible chars
        text = cls.INVISIBLE_PATTERN.sub(
            "",
            text,
        )

        # Replace newlines/tabs
        text = text.replace(
            "\n",
            " ",
        )

        text = text.replace(
            "\r",
            " ",
        )

        text = text.replace(
            "\t",
            " ",
        )

        # Collapse spaces
        text = cls.MULTI_SPACE_PATTERN.sub(
            " ",
            text,
        )

        return text.strip()

    @classmethod
    def clean_many(
        cls,
        texts: List[str],
    ) -> List[str]:

        return [
            cls.clean(text)
            for text in texts
            if text
        ]