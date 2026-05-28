
"""
Enterprise-grade Browser Driver.

Purpose:
- Centralized browser orchestration
- Proxy integration
- Header orchestration
- User-Agent orchestration
- Stealth integration
- Async browser automation

Architecture:
Proxy
↓
Browser Launch
↓
User-Agent Generation
↓
Header Injection
↓
Stealth Protection
↓
Browser Page
↓
Scraping

Design Goals:
- Scalable
- Modular
- Async-first
- Production-ready
"""

from __future__ import annotations

from typing import Optional

from playwright.async_api import (
    async_playwright,
    Browser,
    BrowserContext,
    Page,
)

from browser.headers import HeaderManager
from browser.stealth import StealthManager

from utils.logger import (
    logger,
    log_json,
)


# =========================================================
# Browser Driver
# =========================================================

class BrowserDriver:
    """
    Enterprise browser orchestration layer.
    """

    # =====================================================
    # Initialization
    # =====================================================

    def __init__(
        self,
        proxy: Optional[str] = None,
    ):

        self.proxy = proxy

        self.playwright = None

        self.browser: Optional[
            Browser
        ] = None

        self.context: Optional[
            BrowserContext
        ] = None

        self.page: Optional[
            Page
        ] = None

        # ---------------------------------------------
        # Managers
        # ---------------------------------------------

        self.header_manager = (
            HeaderManager()
        )

        self.stealth_manager = (
            StealthManager()
        )

        logger.info(
            "BrowserDriver initialized"
        )

    # =====================================================
    # Start Browser
    # =====================================================

    async def start(self) -> Page:
        """
        Start browser system.

        Workflow:
        Proxy
        ↓
        Launch Browser
        ↓
        Generate Headers
        ↓
        Create Context
        ↓
        Create Page
        ↓
        Apply Stealth
        """

        try:

            logger.info(
                "Starting browser system"
            )

            # -----------------------------------------
            # Playwright Engine
            # -----------------------------------------

            self.playwright = (
                await async_playwright()
                .start()
            )

            # -----------------------------------------
            # Browser Launch Config
            # -----------------------------------------

            launch_args = {
                "headless": False,
            }

            # -----------------------------------------
            # Proxy Support
            # -----------------------------------------

            if self.proxy:

                logger.info(
                    f"Using proxy -> "
                    f"{self.proxy}"
                )

                proxy_parts = (
                    self.proxy.replace(
                        "http://",
                        ""
                    )
                )

                creds, host = (
                    proxy_parts.split("@")
                )

                username, password = (
                    creds.split(":")
                )

                launch_args["proxy"] = {

                    "server":
                        f"http://{host}",

                    "username":
                        username,

                    "password":
                        password,
                }

            # -----------------------------------------
            # Launch Browser
            # -----------------------------------------

            self.browser = (
                await self.playwright
                .chromium
                .launch(
                    executable_path=(
                        r"C:\Program Files"
                        r"\Google\Chrome"
                        r"\Application"
                        r"\chrome.exe"
                    ),
                    **launch_args
                )
            )

            logger.info(
                "Browser launched"
            )

            # -----------------------------------------
            # Generate Browser Headers
            # -----------------------------------------

            header_profile = (
                self.header_manager
                .generate()
            )

            logger.info(
                "Generated browser headers"
            )

            log_json(
                level="INFO",
                message=(
                    "Browser identity created"
                ),
                extra={
                    "browser":
                        header_profile
                        .browser_profile
                        .browser,

                    "platform":
                        header_profile
                        .browser_profile
                        .platform,
                },
            )

            # -----------------------------------------
            # Create Browser Context
            # -----------------------------------------

            self.context = (
                await self.browser
                .new_context(

                    user_agent=(
                        header_profile
                        .browser_profile
                        .user_agent
                    ),

                    extra_http_headers=(
                        header_profile
                        .headers
                    ),
                )
            )

            logger.info(
                "Browser context created"
            )

            # -----------------------------------------
            # Create Page
            # -----------------------------------------

            self.page = (
                await self.context
                .new_page()
            )

            logger.info(
                "Browser page created"
            )

            # -----------------------------------------
            # Apply Stealth
            # -----------------------------------------

            await self.stealth_manager.apply(
                self.page
            )

            logger.info(
                "Stealth protections applied"
            )

            logger.info(
                "Browser system ready"
            )

            return self.page

        except Exception as e:

            logger.error(
                f"Browser start failed -> {e}"
            )

            raise

    # =====================================================
    # Open URL
    # =====================================================

    async def open(
        self,
        url: str,
    ) -> None:
        """
        Open target URL.
        """

        try:

            logger.info(
                f"Opening URL -> {url}"
            )

            await self.page.goto(
                url,
                wait_until="networkidle",
            )

            logger.info(
                "Page loaded successfully"
            )

        except Exception as e:

            logger.error(
                f"Open URL failed -> {e}"
            )

            raise

    # =====================================================
    # Get HTML
    # =====================================================

    async def get_html(self) -> str:
        """
        Return page HTML.
        """

        return await self.page.content()

    # =====================================================
    # Screenshot
    # =====================================================

    async def screenshot(
        self,
        path: str = (
            "data/screenshot.png"
        ),
    ) -> None:
        """
        Save browser screenshot.
        """

        try:

            await self.page.screenshot(
                path=path,
                full_page=True,
            )

            logger.info(
                f"Screenshot saved -> "
                f"{path}"
            )

        except Exception as e:

            logger.error(
                f"Screenshot failed -> {e}"
            )

            raise

    # =====================================================
    # Close Browser
    # =====================================================

    async def close(self) -> None:
        """
        Shutdown browser system safely.
        """

        try:

            logger.info(
                "Closing browser system"
            )

            if self.browser:

                await self.browser.close()

            if self.playwright:

                await self.playwright.stop()

            logger.info(
                "Browser system closed"
            )

        except Exception as e:

            logger.error(
                f"Browser close failed -> {e}"
            )