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
    print("\n========== LEAD ==========")
    data = result.data

    print(f"URL          : {result.url}")
    print(f"Success      : {result.success}")

    print("\n--- Contact ---")
    print(f"Emails       : {data.get('email', [])}")
    print(f"Phones       : {data.get('phone', [])}")
    print(f"LinkedIn     : {data.get('linkedin', [])}")
    print(f"Websites     : {data.get('website', [])}")

    print("\n--- Company ---")
    print(f"Name         : {data.get('company_name', '')}")
    print(f"Industry     : {data.get('industry', '')}")
    print(f"CEO          : {data.get('ceo_name', '')}")
    print(f"Founder      : {data.get('founder_name', '')}")
    print(f"Description  : {data.get('description', '')}")

    print("\n--- Address ---")
    print(f"Address      : {data.get('address', '')}")

    print("\n==========================")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        type=str,
        default="https://ascentialabs.com/about-us",        # ← your default URL
    )
    parser.add_argument(
    "--fields",
    nargs="+",
    default=[
        "email",
        "phone",
        "linkedin",
        "website",

        # DOM Fields
        "title",

        # AI Fields
        "company_name",
        "industry",
        "description",
        "address",
        "ceo_name",
        "founder_name",
    ],
)

    args = parser.parse_args()

    asyncio.run(main(args.url, args.fields))