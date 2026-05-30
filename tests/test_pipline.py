"""
Entry point — pass URL and fields to scrape.

Terminal:
    python run.py --url "https://example.com" --fields email phone title

Or edit the defaults below and just run:
    python run.py
"""

import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import asyncio
import argparse

from browser.proxy import ProxyManager
from extractors.ScrappingPipline import ScrapingPipeline
from utils.logger import logger


async def main(url: str, fields: list[str]):

    # -----------------------------------
    # Proxy Layer
    # -----------------------------------

    proxy_manager = ProxyManager()

    await proxy_manager.initialize()

    proxy = proxy_manager.get_random_proxy()

    logger.info(f"Selected proxy -> {proxy}")

    # -----------------------------------
    # Scrape
    # -----------------------------------

    result = await ScrapingPipeline.scrape(
        url=url,
        fields=fields,
        proxy=proxy,
    )

    # -----------------------------------
    # Output
    # -----------------------------------

    print("\n--- Result ---")
    print(f"URL     : {result.url}")
    print(f"Proxy   : {proxy}")
    print(f"Success : {result.success}")

    for field, value in result.data.items():
        print(f"{field:15} : {value}")

    if result.error:
        print(f"Error   : {result.error}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--url",
        type=str,
        default="https://www.lakshmimills.com/contact-us/",        # ← your default URL
    )

    parser.add_argument(
        "--fields",
        nargs="+",
        default=["email", "phone", "title" , "linkedin"],  # ← your default fields
    )

    args = parser.parse_args()

    asyncio.run(main(args.url, args.fields))