from browser.proxy import ProxyManager
import asyncio


async def main():
    proxy_manager = ProxyManager()
    await proxy_manager.initialize()

    proxy = proxy_manager.get_random_proxy()

    if proxy:
        is_alive = await proxy_manager.validate_proxy(proxy)  # ← await added
        print("Proxy:", proxy)
        print("Alive:", is_alive)


asyncio.run(main())