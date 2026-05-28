# import asyncio

# from browser.proxy import ProxyManager
# from browser.driver import BrowserDriver


# async def main():

#     proxy_manager = ProxyManager()

#     await proxy_manager.initialize()

#     proxy = proxy_manager.get_random_proxy()

#     browser = BrowserDriver(proxy=proxy)

#     await browser.start()

#     await browser.open(
#         "https://api.ipify.org?format=json"
#     )

#     input("Press Enter to close browser...")

#     await browser.close()


# asyncio.run(main())

import asyncio

from browser.proxy import ProxyManager
from browser.driver import BrowserDriver

from utils.logger import logger


async def main():

    browser = None

    try:

        # -----------------------------------
        # Initialize Proxy Layer
        # -----------------------------------

        proxy_manager = ProxyManager()

        await proxy_manager.initialize()

        proxy = (
            proxy_manager
            .get_random_proxy()
        )

        logger.info(
            f"Selected proxy -> {proxy}"
        )

        # -----------------------------------
        # Initialize Browser Layer
        # -----------------------------------

        browser = BrowserDriver(
            proxy=proxy
        )

        await browser.start()

        # -----------------------------------
        # Open Target
        # -----------------------------------

        await browser.open(
            "https://api.ipify.org?format=json"
        )

        logger.info(
            "Scraping workflow started"
        )

        input(
            "Press Enter to close..."
        )

    except Exception as e:

        logger.error(
            f"Application failed -> {e}"
        )

    finally:

        # -----------------------------------
        # Cleanup Resources
        # -----------------------------------

        if browser:

            await browser.close()

        logger.info(
            "Application shutdown complete"
        )


if __name__ == "__main__":

    asyncio.run(main())