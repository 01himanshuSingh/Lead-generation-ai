import asyncio

from browser.proxy import ProxyManager
from browser.driver import BrowserDriver


async def main():

    proxy_manager = ProxyManager()

    await proxy_manager.initialize()

    proxy = proxy_manager.get_random_proxy()

    browser = BrowserDriver(proxy=proxy)

    await browser.start()

    await browser.open(
        "https://api.ipify.org?format=json"
    )

    input("Press Enter to close browser...")

    await browser.close()


asyncio.run(main())