"""
Enterprise-grade Scraping Pipeline.

Purpose:
- Single entrypoint facade for scraping workflows
- Wires BrowserDriver + ExtractionOrchestrator
- Typed result contract
- Async-first, production-ready

Architecture:

    Caller
      ↓
    ScrapingPipeline.run(url, fields)
      ↓
    BrowserDriver          ← browser lifecycle
      ├── start()
      ├── open(url)
      └── get_html()
      ↓
    ExtractionOrchestrator ← data extraction
      └── extract(html, fields)
      ↓
    ScrapeResult           ← typed output contract

Design Goals:
- Single responsibility per layer
- Zero coupling between browser and extractor
- Context-manager support (auto-close)
- Reusable across CLI, API, worker queues
- Extensible without touching internals

Usage:

    # One-shot
    result = await ScrapingPipeline.scrape(
        url="https://example.com",
        fields=["email", "phone", "title"],
    )

    # Reusable session (better for bulk)
    async with ScrapingPipeline() as pipeline:
        r1 = await pipeline.run("https://site1.com", ["email"])
        r2 = await pipeline.run("https://site2.com", ["email", "phone"])
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from browser.driver import BrowserDriver
from extractors.orchestrator import ExtractionOrchestrator
from utils.logger import logger, log_json
from storage.excel_exporter import ExcelExporter
from urllib.parse import urlparse

# =========================================================
# Result Contract
# =========================================================

@dataclass
class ScrapeResult:
    """
    Typed output contract for a single scrape run.

    Guarantees a predictable shape regardless of
    which extractors ran internally.
    """

    url: str
    fields_requested: List[str]
    data: Dict[str, Any]
    success: bool
    error: Optional[str] = None

    # --------------------------------------------------
    # Convenience accessors
    # --------------------------------------------------

    def get(self, field: str, default: Any = None) -> Any:
        """Safe field accessor — never raises KeyError."""
        return self.data.get(field, default)

    def __repr__(self) -> str:
        status = "OK" if self.success else f"FAILED({self.error})"
        return (
            f"ScrapeResult("
            f"url={self.url!r}, "
            f"status={status}, "
            f"fields={list(self.data.keys())})"
        )


# =========================================================
# Scraping Pipeline
# =========================================================

class ScrapingPipeline:
    """
    Facade that coordinates BrowserDriver
    and ExtractionOrchestrator into a single
    cohesive scraping workflow.

    Responsibilities:
    - Manage browser lifecycle
    - Delegate navigation to BrowserDriver
    - Delegate extraction to ExtractionOrchestrator
    - Return a typed ScrapeResult

    NOT responsible for:
    - How the browser renders pages  (BrowserDriver)
    - How data is extracted          (ExtractionOrchestrator)
    - Storing or processing results  (caller's concern)
    """

    # =====================================================
    # Initialization
    # =====================================================

    def __init__(
        self,
        proxy: Optional[str] = None,
        screenshot: bool = False,
        screenshot_dir: str = "data/screenshots",
    ):
        """
        Args:
            proxy:          Optional proxy string.
                            Format: "http://user:pass@host:port"

            screenshot:     Capture a screenshot after each page load.

            screenshot_dir: Directory to store screenshots.
        """

        self.proxy = proxy
        self.screenshot = screenshot
        self.screenshot_dir = screenshot_dir

        # --------------------------------------------------
        # Core subsystems — injected, not coupled
        # --------------------------------------------------

        self._driver = BrowserDriver(proxy=proxy)
        self._orchestrator = ExtractionOrchestrator()

        # --------------------------------------------------
        # Lifecycle state
        # --------------------------------------------------

        self._started = False

        logger.info("ScrapingPipeline initialized")

    # =====================================================
    # Context Manager Support
    # =====================================================

    async def __aenter__(self) -> "ScrapingPipeline":
        await self._boot()
        return self

    async def __aexit__(self, *_) -> None:
        await self._shutdown()

    # =====================================================
    # Lifecycle
    # =====================================================

    async def _boot(self) -> None:
        """Start the browser system once."""

        if self._started:
            return

        logger.info("Booting ScrapingPipeline")

        await self._driver.start()
        self._started = True

        logger.info("ScrapingPipeline ready")

    async def _shutdown(self) -> None:
        """Gracefully close the browser."""

        logger.info("Shutting down ScrapingPipeline")

        await self._driver.close()
        self._started = False

        logger.info("ScrapingPipeline shutdown complete")

    # =====================================================
    # Core Run
    # =====================================================

    async def run(
        self,
        url: str,
        fields: List[str],
    ) -> ScrapeResult:
        """
        Navigate to `url` and extract `fields`.

        Args:
            url:    Target URL to scrape.
            fields: List of fields to extract.
                    Supported values (mix freely):
                        Regex:  "email", "phone", "linkedin",
                                "website", "instagram"
                        DOM:    "title", "meta", "open_graph",
                                "schema", "visible_text"

        Returns:
            ScrapeResult with .data dict keyed by field name.

        Example:
            result = await pipeline.run(
                url="https://example.com",
                fields=["email", "phone", "title"],
            )
            print(result.get("email"))
        """

        logger.info(
            f"Pipeline run -> url={url} fields={fields}"
        )

        if not self._started:
            await self._boot()

        try:

            # ---------------------------------------------
            # Step 1: Navigate
            # ---------------------------------------------

            await self._driver.open(url)

            logger.info("Navigation complete")

            # ---------------------------------------------
            # Step 2: Optional Screenshot
            # ---------------------------------------------

            if self.screenshot:

                import os
                import re

                safe_name = re.sub(
                    r"[^\w]", "_", url
                )[:80]

                path = os.path.join(
                    self.screenshot_dir,
                    f"{safe_name}.png",
                )

                os.makedirs(
                    self.screenshot_dir,
                    exist_ok=True,
                )

                await self._driver.screenshot(path)

            # ---------------------------------------------
            # Step 3: Get HTML
            # ---------------------------------------------

            html = await self._driver.get_html()

            logger.info(
                f"HTML captured -> {len(html)} chars"
            )

            # ---------------------------------------------
            extracted = await (
    self._orchestrator.extract(
        url=url,
        html=html,
        fields=fields,
    )
)

            parsed = urlparse(url)

            extracted.source_url = url

            extracted.company.website = (
                f"{parsed.scheme}://{parsed.netloc}"
            )

            extracted.contact.websites = [
                f"{parsed.scheme}://{parsed.netloc}"
            ]
            extracted.log()

            # Map LeadModel fields to a dictionary containing the requested fields
            extracted_dict = {}
            for field in fields:
                if field == "email":
                    extracted_dict["email"] = extracted.contact.emails
                elif field == "phone":
                    extracted_dict["phone"] = extracted.contact.phones
                elif field == "linkedin":
                    extracted_dict["linkedin"] = extracted.contact.linkedin_urls
                elif field == "website":
                    extracted_dict["website"] = extracted.contact.websites
                elif field == "company_name":
                    extracted_dict["company_name"] = extracted.company.name
                elif field == "address":
                    extracted_dict["address"] = extracted.address.full_address
                elif field in ["title", "meta", "schema", "open_graph", "visible_text"]:
                    extracted_dict[field] = extracted.metadata.get(field)
                else:
                    extracted_dict[field] = getattr(extracted, field, None)

            # ---------------------------------------------
            # Step 5: Build Result
            # ---------------------------------------------

            result = ScrapeResult(
                url=url,
                fields_requested=fields,
                data=extracted_dict,
                success=True,
            )

            ExcelExporter.export_lead(
    extracted
)

            log_json(
                level="INFO",
                message="Pipeline run success",
                extra={
                    "url": url,
                    "fields_found": list(extracted_dict.keys()),
                },
            )

            return result

        except Exception as e:

            logger.error(
                f"Pipeline run failed -> url={url} error={e}"
            )

            return ScrapeResult(
                url=url,
                fields_requested=fields,
                data={},
                success=False,
                error=str(e),
            )

    # =====================================================
    # Bulk Run
    # =====================================================

    async def run_bulk(
        self,
        targets: List[Dict[str, Any]],
    ) -> List[ScrapeResult]:
        """
        Scrape multiple URLs sequentially
        in a single browser session.

        Args:
            targets: List of dicts, each with:
                     {
                         "url": "https://...",
                         "fields": ["email", "phone"]
                     }

        Returns:
            List[ScrapeResult] in same order as input.

        Example:
            results = await pipeline.run_bulk([
                {"url": "https://a.com", "fields": ["email"]},
                {"url": "https://b.com", "fields": ["email", "phone"]},
            ])
        """

        logger.info(
            f"Bulk run -> {len(targets)} targets"
        )

        results = []

        for target in targets:

            result = await self.run(
                url=target["url"],
                fields=target["fields"],
            )

            results.append(result)

        logger.info(
            f"Bulk run complete -> "
            f"{sum(1 for r in results if r.success)}"
            f"/{len(results)} succeeded"
        )

        return results

    # =====================================================
    # Static One-Shot Helper
    # =====================================================

    @staticmethod
    async def scrape(
        url: str,
        fields: List[str],
        proxy: Optional[str] = None,
        screenshot: bool = False,
    ) -> ScrapeResult:
        """
        Convenience one-shot method.

        Boots browser, scrapes, closes browser.
        Best for single URL calls.

        For bulk / repeated calls use the
        context-manager form to reuse the browser.

        Example:
            result = await ScrapingPipeline.scrape(
                url="https://example.com",
                fields=["email", "phone", "title"],
            )
        """

        pipeline = ScrapingPipeline(
            proxy=proxy,
            screenshot=screenshot,
        )

        async with pipeline:
            return await pipeline.run(url, fields)