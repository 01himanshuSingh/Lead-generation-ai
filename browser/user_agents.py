"""
Scalable User-Agent management system.

Purpose:
- Realistic browser fingerprint rotation
- Cross-platform browser identity generation
- Centralized User-Agent management
- Production scraping architecture

Used by:
- HeaderManager
- BrowserContext
- Fingerprint systems
- Session managers

Scalable Features:
- Browser filtering
- Platform filtering
- Rotation strategies
- Static pools fallback
- Randomization layer
- Future fingerprint expansion
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List, Optional

# pyrefly: ignore [missing-import]
from fake_useragent import UserAgent

from utils.logger import logger


# -----------------------------
# Browser Profile Model
# -----------------------------

@dataclass(slots=True)
class BrowserProfile:
    """
    Represents a browser identity profile.
    """

    user_agent: str
    browser: str
    platform: str
    device_type: str


# -----------------------------
# Static Fallback Pool
# -----------------------------

STATIC_USER_AGENTS = [
    {
        "browser": "chrome",
        "platform": "windows",
        "device_type": "desktop",
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
    },
    {
        "browser": "chrome",
        "platform": "linux",
        "device_type": "desktop",
        "user_agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
    },
    {
        "browser": "firefox",
        "platform": "windows",
        "device_type": "desktop",
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) "
            "Gecko/20100101 Firefox/125.0"
        ),
    },
]


# -----------------------------
# User-Agent Manager
# -----------------------------

class UserAgentManager:
    """
    Enterprise-grade User-Agent manager.

    Responsibilities:
    - Generate realistic browser identities
    - Randomize browser fingerprints
    - Provide fallback mechanisms
    - Normalize scraping fingerprints

    Design Goals:
    - Scalable
    - Modular
    - Extendable
    - Anti-detection aware
    """

    def __init__(self):

        self.ua = UserAgent()

        logger.info("UserAgentManager initialized")

    # ---------------------------------
    # Main Public Generator
    # ---------------------------------

    def generate(
        self,
        browser: Optional[str] = None,
        platform: Optional[str] = None,
        device_type: str = "desktop",
    ) -> BrowserProfile:
        """
        Generate randomized browser profile.

        Args:
            browser:
                chrome | firefox | edge | safari

            platform:
                windows | linux | macos

            device_type:
                desktop | mobile

        Returns:
            BrowserProfile
        """

        try:

            user_agent = self._dynamic_user_agent(browser)

            profile = BrowserProfile(
                user_agent=user_agent,
                browser=browser or "chrome",
                platform=platform or "windows",
                device_type=device_type,
            )

            logger.info(
                f"Generated User-Agent profile -> "
                f"{profile.browser} | "
                f"{profile.platform}"
            )

            return profile

        except Exception as e:

            logger.warning(
                f"Dynamic User-Agent failed -> {e}"
            )

            logger.warning(
                "Using static fallback User-Agent pool"
            )

            return self._fallback_profile()

    # ---------------------------------
    # Dynamic User-Agent Generator
    # ---------------------------------

    def _dynamic_user_agent(
        self,
        browser: Optional[str],
    ) -> str:
        """
        Generate dynamic User-Agent.

        Uses fake-useragent internally.
        """

        if browser == "firefox":
            return self.ua.firefox

        if browser == "edge":
            return self.ua.edge

        if browser == "safari":
            return self.ua.safari

        return self.ua.chrome

    # ---------------------------------
    # Static Fallback System
    # ---------------------------------

    def _fallback_profile(self) -> BrowserProfile:
        """
        Return safe static fallback profile.
        """

        selected = random.choice(
            STATIC_USER_AGENTS
        )

        return BrowserProfile(
            user_agent=selected["user_agent"],
            browser=selected["browser"],
            platform=selected["platform"],
            device_type=selected["device_type"],
        )

    # ---------------------------------
    # Batch Generation
    # ---------------------------------

    def generate_batch(
        self,
        count: int = 5,
    ) -> List[BrowserProfile]:
        """
        Generate multiple profiles.

        Useful for:
        - worker pools
        - concurrent scraping
        - session rotation
        """

        return [
            self.generate()
            for _ in range(count)
        ]

    # ---------------------------------
    # Mobile Profiles
    # ---------------------------------

    def mobile_profile(self) -> BrowserProfile:
        """
        Generate mobile browser identity.
        """

        return BrowserProfile(
            user_agent=(
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 "
                "like Mac OS X) AppleWebKit/605.1.15 "
                "(KHTML, like Gecko) Version/17.0 "
                "Mobile/15E148 Safari/604.1"
            ),
            browser="safari",
            platform="ios",
            device_type="mobile",
        )