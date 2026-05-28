"""
Enterprise-grade Header Management System.

Purpose:
- Generate realistic browser headers
- Match browser fingerprints
- Reduce bot detection
- Centralize request identity logic
- Support scalable scraping infrastructure

Architecture Goals:
- Modular
- Stateless
- Async compatible
- Extendable
- Production-ready

Used By:
- Playwright Browser Contexts
- HTTP Clients
- Session Managers
- Browser Drivers
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List, Optional

# pyrefly: ignore [missing-import]
from browser.user_agents import (
    BrowserProfile,
    UserAgentManager,
)

from utils.logger import logger


# =========================================================
# Header Profile Model
# =========================================================

@dataclass(slots=True)
class HeaderProfile:
    """
    Represents browser header identity.
    """

    headers: Dict[str, str]
    browser_profile: BrowserProfile


# =========================================================
# Header Manager
# =========================================================

class HeaderManager:
    """
    Centralized browser header generation system.

    Responsibilities:
    - Browser-like request headers
    - Locale randomization
    - Browser metadata spoofing
    - Header normalization
    - Fingerprint consistency

    Design:
    - Stateless
    - Scalable
    - Reusable
    """

    # -----------------------------------------------------
    # Initialization
    # -----------------------------------------------------

    def __init__(self):

        self.user_agent_manager = (
            UserAgentManager()
        )

        logger.info(
            "HeaderManager initialized"
        )

    # =====================================================
    # Public API
    # =====================================================

    def generate(
        self,
        browser: Optional[str] = "chrome",
        platform: Optional[str] = "windows",
        mobile: bool = False,
    ) -> HeaderProfile:
        """
        Generate realistic browser headers.

        Args:
            browser:
                chrome | firefox | edge | safari

            platform:
                windows | linux | macos

            mobile:
                Generate mobile browser profile

        Returns:
            HeaderProfile
        """

        try:

            # ---------------------------------------------
            # Browser Identity
            # ---------------------------------------------

            if mobile:

                profile = (
                    self.user_agent_manager
                    .mobile_profile()
                )

            else:

                profile = (
                    self.user_agent_manager
                    .generate(
                        browser=browser,
                        platform=platform,
                    )
                )

            # ---------------------------------------------
            # Build Headers
            # ---------------------------------------------

            headers = self._build_headers(
                profile
            )

            logger.info(
                "Generated realistic "
                "browser headers"
            )

            return HeaderProfile(
                headers=headers,
                browser_profile=profile,
            )

        except Exception as e:

            logger.error(
                f"Header generation failed -> {e}"
            )

            raise

    # =====================================================
    # Internal Header Builder
    # =====================================================

    def _build_headers(
        self,
        profile: BrowserProfile,
    ) -> Dict[str, str]:
        """
        Construct realistic browser headers.
        """

        # ---------------------------------------------
        # Language Pools
        # ---------------------------------------------

        languages = [
            "en-US,en;q=0.9",
            "en-GB,en;q=0.8",
            "en-IN,en;q=0.9",
        ]

        # ---------------------------------------------
        # Accept Headers
        # ---------------------------------------------

        accept_headers = [
            (
                "text/html,"
                "application/xhtml+xml,"
                "application/xml;q=0.9,"
                "image/avif,image/webp,"
                "*/*;q=0.8"
            )
        ]

        # ---------------------------------------------
        # Base Browser Headers
        # ---------------------------------------------

        headers = {

            # =========================================
            # Browser Identity
            # =========================================

            "User-Agent":
                profile.user_agent,

            # =========================================
            # Browser Accept
            # =========================================

            "Accept":
                random.choice(
                    accept_headers
                ),

            "Accept-Language":
                random.choice(
                    languages
                ),

            "Accept-Encoding":
                "gzip, deflate, br",

            # =========================================
            # Browser Navigation
            # =========================================

            "Connection":
                "keep-alive",

            "Upgrade-Insecure-Requests":
                "1",

            # =========================================
            # Fetch Metadata
            # =========================================

            "Sec-Fetch-Dest":
                "document",

            "Sec-Fetch-Mode":
                "navigate",

            "Sec-Fetch-Site":
                "none",

            "Sec-Fetch-User":
                "?1",

            # =========================================
            # Cache
            # =========================================

            "Cache-Control":
                "max-age=0",
        }

        # ---------------------------------------------
        # Chromium Browser Headers
        # ---------------------------------------------

        if profile.browser in (
            "chrome",
            "edge",
        ):

            headers.update({

                "sec-ch-ua":
                    (
                        '"Chromium";v="124", '
                        '"Google Chrome";v="124", '
                        '"Not-A.Brand";v="99"'
                    ),

                "sec-ch-ua-mobile":
                    "?0",

                "sec-ch-ua-platform":
                    f'"{profile.platform}"',
            })

        return headers

    # =====================================================
    # Batch Header Generation
    # =====================================================

    def generate_batch(
        self,
        count: int = 5,
    ) -> List[HeaderProfile]:
        """
        Generate multiple browser identities.

        Useful for:
        - Worker pools
        - Session rotation
        - Concurrent scraping
        """

        return [
            self.generate()
            for _ in range(count)
        ]

    # =====================================================
    # Lightweight API Headers
    # =====================================================

    def api_headers(self) -> Dict[str, str]:
        """
        Lightweight API request headers.

        Used for:
        - REST APIs
        - JSON endpoints
        - Internal APIs
        """

        profile = (
            self.user_agent_manager
            .generate()
        )

        return {

            "User-Agent":
                profile.user_agent,

            "Accept":
                "application/json",

            "Connection":
                "keep-alive",
        }

    # =====================================================
    # Mobile Browser Headers
    # =====================================================

    def mobile_headers(self) -> HeaderProfile:
        """
        Generate mobile browser headers.
        """

        return self.generate(
            mobile=True
        )