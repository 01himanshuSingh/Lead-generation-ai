# """Browser automation driver initialization."""
# from playwright.async_api import async_playwright, Browser, BrowserContext, Page
# from config import settings
# from utils.logger import logger, log_json

# from typing import Optional


# class BrowserDriver:
#     """
#     Scalable Playwright browser manager.
#     Handles:
#     - Chromium launch
#     - headless mode
#     - proxy injection
#     - browser context creation
#     """

#     def __init__(self):

#         self.playwright = None
#         self.browser: Optional[Browser] = None
#         self.context: Optional[BrowserContext] = None
#         self.page: Optional[Page] = None

#     async def start(self):

#         logger.info("Starting Playwright browser")

#         log_json(
#             level="INFO",
#             message="Launching browser",
#         )

#         self.playwright = await async_playwright().start()

#         self.browser = await self.playwright.chromium.launch(
#             headless=settings.HEADLESS,

#             proxy={
#                 "server": f"http://{settings.PROXY_HOST}:{settings.PROXY_PORT}",
#                 "username": settings.PROXY_USER,
#                 "password": settings.PROXY_PASS,
#             },

#             args=[
#                 "--disable-blink-features=AutomationControlled",
#                 "--disable-web-security",
#                 "--disable-features=IsolateOrigins,site-per-process",
#                 "--disable-dev-shm-usage",
#                 "--no-sandbox",
#             ],
#         )

#         self.context = await self.browser.new_context(
#             ignore_https_errors=True,

#             viewport={
#                 "width": 1280,
#                 "height": 720,
#             },

#             user_agent=(
#                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                 "AppleWebKit/537.36 (KHTML, like Gecko) "
#                 "Chrome/124.0.0.0 Safari/537.36"
#             ),

#             java_script_enabled=True,
#         )

#         self.page = await self.context.new_page()

#         logger.info("Browser started successfully")

#         log_json(
#             level="INFO",
#             message="Browser launched successfully",
#         )

#         return self.page

#     async def open(self, url: str):

#         if not self.page:
#             raise ValueError("Browser page not initialized")

#         logger.info(f"Opening URL: {url}")

#         await self.page.goto(
#             url,
#             wait_until="networkidle",
#             timeout=60000,
#         )

#         log_json(
#             level="INFO",
#             message="URL opened successfully",
#             extra={"url": url},
#         )

#         return self.page

#     async def get_html(self):

#         if not self.page:
#             raise ValueError("Page not initialized")

#         return await self.page.content()

#     async def screenshot(self, path: str = "data/screenshot.png"):

#         if self.page:
#             await self.page.screenshot(path=path)

#     async def close(self):

#         logger.info("Closing browser")

#         if self.context:
#             await self.context.close()

#         if self.browser:
#             await self.browser.close()

#         if self.playwright:
#             await self.playwright.stop()

#         log_json(
#             level="INFO",
#             message="Browser closed successfully",
#         )


from playwright.async_api import async_playwright


class BrowserDriver:

    def __init__(self, proxy=None):

        self.proxy = proxy

        self.playwright = None
        self.browser = None
        self.page = None

    async def start(self):

        self.playwright = await async_playwright().start()

        launch_args = {
            "headless": False,
        }

        # Proxy support
        if self.proxy:

            print(f"Using proxy: {self.proxy}")

            proxy_parts = self.proxy.replace(
                "http://",
                ""
            )

            creds, host = proxy_parts.split("@")

            username, password = creds.split(":")

            launch_args["proxy"] = {
                "server": f"http://{host}",
                "username": username,
                "password": password,
            }

        self.browser = await self.playwright.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            **launch_args
        )

        self.page = await self.browser.new_page()

        print("Browser started")

        return self.page

    async def open(self, url):

        print(f"Opening: {url}")

        await self.page.goto(url)

    async def get_html(self):

        return await self.page.content()

    async def screenshot(self, path="screenshot.png"):

        await self.page.screenshot(path=path)

    async def close(self):

        if self.browser:

            await self.browser.close()

        if self.playwright:

            await self.playwright.stop()