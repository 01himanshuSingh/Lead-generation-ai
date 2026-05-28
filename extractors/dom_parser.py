"""DOM Parsing and query selector logic.

Enterprise-grade DOM Parsing Engine.

Purpose:
- Structured HTML parsing
- Metadata extraction
- schema.org parsing
- OpenGraph extraction
- Visible text extraction

Architecture:
Rendered HTML
    ↓
BeautifulSoup Parsing
    ↓
Structured DOM Extraction
    ↓
Normalized Output
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

# pyrefly: ignore [missing-import]
from bs4 import BeautifulSoup

from utils.logger import logger


# =========================================================
# DOM Extraction Result
# =========================================================

@dataclass(slots=True)
class DOMExtractionResult:

    title: str
    meta: Dict[str, str]
    open_graph: Dict[str, str]
    schema_data: List[dict]
    visible_text: str


# =========================================================
# DOM Parser Engine
# =========================================================

class DOMParser:

    def __init__(self):

        logger.info(
            "DOMParser initialized"
        )

    # =====================================================
    # Main Parse API
    # =====================================================

    def parse(
        self,
        html: str,
    ) -> DOMExtractionResult:

        logger.info(
            "Starting DOM parsing"
        )

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        title = self._extract_title(
            soup
        )

        meta = self._extract_meta_tags(
            soup
        )

        open_graph = (
            self._extract_open_graph(
                soup
            )
        )

        schema_data = (
            self._extract_schema(
                soup
            )
        )

        visible_text = (
            self._extract_visible_text(
                soup
            )
        )

        logger.info(
            "DOM parsing completed"
        )

        return DOMExtractionResult(
            title=title,
            meta=meta,
            open_graph=open_graph,
            schema_data=schema_data,
            visible_text=visible_text,
        )

    # =====================================================
    # Title Extraction
    # =====================================================

    def _extract_title(
        self,
        soup: BeautifulSoup,
    ) -> str:

        if soup.title:

            return soup.title.text.strip()

        return ""

    # =====================================================
    # Meta Tags Extraction
    # =====================================================

    def _extract_meta_tags(
        self,
        soup: BeautifulSoup,
    ) -> Dict[str, str]:

        meta_data = {}

        tags = soup.find_all("meta")

        for tag in tags:

            name = (
                tag.get("name")
                or tag.get("property")
            )

            content = tag.get("content")

            if name and content:

                meta_data[name] = content

        return meta_data

    # =====================================================
    # Open Graph Extraction
    # =====================================================

    def _extract_open_graph(
        self,
        soup: BeautifulSoup,
    ) -> Dict[str, str]:

        og_data = {}

        tags = soup.find_all(
            "meta",
            property=True
        )

        for tag in tags:

            prop = tag.get("property")

            if (
                prop
                and prop.startswith("og:")
            ):

                og_data[prop] = (
                    tag.get("content", "")
                )

        return og_data

    # =====================================================
    # schema.org Extraction
    # =====================================================

    def _extract_schema(
        self,
        soup: BeautifulSoup,
    ) -> List[dict]:

        schema_data = []

        scripts = soup.find_all(
            "script",
            type="application/ld+json"
        )

        for script in scripts:

            try:

                schema_data.append(
                    script.string
                )

            except Exception:

                continue

        return schema_data

    # =====================================================
    # Visible Text Extraction
    # =====================================================

    def _extract_visible_text(
        self,
        soup: BeautifulSoup,
    ) -> str:

        for tag in soup([
            "script",
            "style",
            "noscript",
        ]):

            tag.extract()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        return text