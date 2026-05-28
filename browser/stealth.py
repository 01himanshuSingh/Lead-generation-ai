"""
Anti-bot detection stealth logic.

Enterprise-grade Browser Stealth System.

Purpose:
- Hide browser automation signals
- Reduce Playwright detection
- Mimic real browser behavior
- Centralize stealth protections
- Support scalable scraping systems

Architecture Goals:
- Modular
- Stateless
- Async compatible
- Extendable
- Production-ready

Used By:
- BrowserDriver
- BrowserContext
- Session Managers
- Scraper Workers

Library:
- playwright-stealth
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from playwright.async_api import Page
# pyrefly: ignore [missing-import]
from playwright_stealth import Stealth

from utils.logger import logger


# =========================================================
# Stealth Configuration Model
# =========================================================

@dataclass(slots=True)
class StealthProfile:
    """
    Represents stealth configuration profile.
    """

    webdriver: bool = True
    chrome_runtime: bool = True
    navigator_languages: bool = True
    navigator_plugins: bool = True
    permissions: bool = True
    webgl_vendor: bool = True
    outerdimensions: bool = True


# =========================================================
# Stealth Manager
# =========================================================

class StealthManager:
    """
    Centralized browser stealth manager.

    Responsibilities:
    - Hide automation fingerprints
    - Patch Playwright detection
    - Normalize browser behavior
    - Apply anti-detection protections

    Design:
    - Stateless
    - Scalable
    - Reusable
    """

    def __init__(
        self,
        profile: Optional[
            StealthProfile
        ] = None,
    ):

        self.profile = (
            profile
            or StealthProfile()
        )

        logger.info(
            "StealthManager initialized"
        )

    # =====================================================
    # Public API
    # =====================================================

    async def apply(
        self,
        page: Page,
    ) -> None:
        """
        Apply stealth protections to page.

        Args:
            page:
                Playwright page instance
        """

        try:

            logger.info(
                "Applying stealth protections"
            )

            # -----------------------------------------
            # Apply playwright-stealth
            # -----------------------------------------

            stealth = Stealth()

            await stealth.apply_stealth_async(
                page
            )

            # -----------------------------------------
            # Additional Custom Patches
            # -----------------------------------------

            await self._patch_webdriver(
                page
            )

            await self._patch_hardware(
                page
            )

            await self._patch_permissions(
                page
            )

            logger.info(
                "Stealth protections applied"
            )

        except Exception as e:

            logger.error(
                f"Stealth apply failed -> {e}"
            )

            raise

    # =====================================================
    # webdriver Patch
    # =====================================================

    async def _patch_webdriver(
        self,
        page: Page,
    ) -> None:
        """
        Hide navigator.webdriver
        """

        if not self.profile.webdriver:
            return

        await page.add_init_script(
            """
            Object.defineProperty(
                navigator,
                'webdriver',
                {
                    get: () => undefined
                }
            );
            """
        )

    # =====================================================
    # Hardware Fingerprint Patch
    # =====================================================

    async def _patch_hardware(
        self,
        page: Page,
    ) -> None:
        """
        Normalize hardware fingerprints.
        """

        await page.add_init_script(
            """
            Object.defineProperty(
                navigator,
                'hardwareConcurrency',
                {
                    get: () => 8
                }
            );

            Object.defineProperty(
                navigator,
                'deviceMemory',
                {
                    get: () => 8
                }
            );
            """
        )

    # =====================================================
    # Permissions Patch
    # =====================================================

    async def _patch_permissions(
        self,
        page: Page,
    ) -> None:
        """
        Normalize permissions behavior.
        """

        if not self.profile.permissions:
            return

        await page.add_init_script(
            """
            const originalQuery =
                window.navigator.permissions.query;

            window.navigator.permissions.query =
                (parameters) => (

                    parameters.name === 'notifications'

                    ? Promise.resolve({
                        state: Notification.permission
                    })

                    : originalQuery(parameters)
                );
            """
        )

    # =====================================================
    # Batch Worker Support
    # =====================================================

    async def apply_batch(
        self,
        pages: list[Page],
    ) -> None:
        """
        Apply stealth to multiple pages.

        Useful for:
        - Concurrent scraping
        - Worker pools
        - Session rotation
        """

        for page in pages:

            await self.apply(page)