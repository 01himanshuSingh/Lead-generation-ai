"""Proxy rotation and management manager."""
import random
# pyrefly: ignore [missing-import]
import aiohttp
from typing import List, Optional

from utils.logger import logger, log_json
from config import settings


class ProxyManager:
    """
    Hybrid proxy management system.

    Priority:
    1. Webshare proxies
    2. Free fallback proxies
    """

    def __init__(self):
        self.proxies: List[str] = []
        self.current_proxy: Optional[str] = None

    def load_webshare_proxies(self):
        """Load Webshare rotating proxy from .env"""

        logger.info("Loading Webshare proxies")

        raw = (
            f"http://"
            f"{settings.PROXY_USER}:"
            f"{settings.PROXY_PASS}@"
            f"{settings.PROXY_HOST}:"
            f"{settings.PROXY_PORT}"
        )

        self.proxies.append(raw)

        log_json(
            level="INFO",
            message="Webshare rotating proxy loaded",
            extra={"count": len(self.proxies)},
        )

    async def load_free_fallback_proxies(self):
        """Simulate proxybroker2 fallback logic."""

        if not settings.USE_FREE_FALLBACK_PROXIES:
            return

        logger.info("Loading fallback free proxies")

        fallback = [
            "http://103.149.162.194:80",
            "http://51.159.115.233:3128",
        ]

        self.proxies.extend(fallback)

        log_json(
            level="INFO",
            message="Fallback proxies loaded",
            extra={"count": len(fallback)},
        )

    def get_random_proxy(self) -> Optional[str]:
        """Rotate random proxy."""

        if not self.proxies:
            logger.warning("No proxies available")
            return None

        self.current_proxy = random.choice(self.proxies)
        logger.info(f"Using proxy: {self.current_proxy}")
        return self.current_proxy

    async def validate_proxy(self, proxy: str) -> bool:
        try:
            auth = aiohttp.BasicAuth(settings.PROXY_USER, settings.PROXY_PASS)
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://httpbin.org/ip",
                    proxy=proxy,
                    proxy_auth=auth,
                    timeout=aiohttp.ClientTimeout(total=settings.PROXY_TIMEOUT),
                ) as response:
                    data = await response.json()
                    real_ip = "your_real_ip"  # hardcode to double check
                    masked_ip = data["origin"]
                    if masked_ip == real_ip:
                        logger.error("⚠️ IP LEAK DETECTED — proxy not working!")
                        return False
                    print(f"✅ Masked IP: {masked_ip} — real IP hidden")
                    return response.status == 200
        except Exception as e:
            logger.warning(f"Dead proxy: {proxy} — {e}")
            return False
    def remove_dead_proxy(self, proxy: str):
        """Remove a dead proxy from the pool."""

        if proxy in self.proxies:
            self.proxies.remove(proxy)
            logger.warning(f"Removed dead proxy: {proxy}")

    async def initialize(self):
        """Initialize proxy pool."""

        self.proxies = []  # reset on re-init
        self.load_webshare_proxies()
        await self.load_free_fallback_proxies()

        logger.info(f"Total proxies loaded: {len(self.proxies)}")