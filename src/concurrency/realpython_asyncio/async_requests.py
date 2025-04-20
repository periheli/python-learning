"""Asynchronously get links embedded in multiple pages' HMTL."""

import asyncio
import logging
import re
import sys
import urllib.error
import urllib.parse
from pathlib import Path
from typing import IO

import aiofiles
import aiohttp
from aiohttp import ClientSession

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)
logging.getLogger("chardet.charsetprober").disabled = True

HREF_REGEX = re.compile(r'href="(.*?)"')


async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    """
    GET request wrapper to fetch page HTML.

    kwargs are passed to `session.request()`.
    """

    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    logger.info("Got response [%s] for URL: %s", resp.status, url)
    html = await resp.text()
    return html


async def parse(url: str, session: ClientSession, **kwargs) -> set:
    """Find HREFs in the HTML of `url`."""
    found = set()
    try:
        html = await fetch_html(url=url, session=session, **kwargs)
    except (
        aiohttp.ClientError,
        aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        logger.error(
            "aiohttp exception for %s [%s]: %s",
            url,
            getattr(e, "status", None),
            getattr(e, "message", None),
        )
        return found
    else:
        for link in HREF_REGEX.findall(html):
            try:
                abslink = urllib.parse.urljoin(url, link)
            except (urllib.error.URLError, ValueError):
                logger.exception("Error parsing URL: %s", link)
                pass
            else:
                found.add(abslink)
        logger.info("Found %d links for %s", len(found), url)
        return found


async def write_one(file: str | Path, url: str, **kwargs) -> None:
    """Write the found HREFs from `url` to `file`."""
    res = await parse(url=url, **kwargs)
    if not res:
        return None
    async with aiofiles.open(file, "a") as f:
        for p in res:
            await f.write(f"{url}\t{p}\n")
        logger.info("Wrote results for source URL: %s", url)


async def bulk_crawl_and_write(file: str | Path, urls: set, **kwargs) -> None:
    """Crawl and write concurrently to `file` for multiple `urls`."""

    async with ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(
                write_one(file=file, url=url, session=session, **kwargs)
            )
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    import pathlib
    import sys

    assert sys.version_info >= (3, 7), "Script requires Python 3.7+"
    here = pathlib.Path(__file__).parent

    with open(here / "urls.txt") as input_file:
        urls = set(map(str.strip, input_file))

    output_path = here / "found_urls.txt"
    with open(output_path, "w") as output_file:
        output_file.write("source_url\tparsed_url\n")

    asyncio.run(bulk_crawl_and_write(file=output_path, urls=urls))
