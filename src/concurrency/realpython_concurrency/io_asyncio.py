import asyncio
import time
from typing import List

import aiohttp


async def main():
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    await download_all_sites(sites)


async def download_site(url: str, session: aiohttp.ClientSession):
    async with session.get(url) as response:
        print(f"Read {len(await response.text())} bytes from {url}")


async def download_all_sites(sites: List[str]):
    async with aiohttp.ClientSession() as session:
        tasks = [download_site(url, session) for url in sites]
        await asyncio.gather(*tasks, return_exceptions=True)
