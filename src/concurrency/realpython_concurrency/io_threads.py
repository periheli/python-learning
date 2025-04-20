import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List

import requests

thread_local = threading.local()


def main(num_threads: int = 5):
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    download_all_sites(sites, num_threads=num_threads)


def get_session_for_thread():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url: str):
    session = get_session_for_thread()
    with session.get(url) as response:
        print(f"Read {len(response.content)} bytes from {url}")


def download_all_sites(sites: List[str], num_threads: int = 5):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(download_site, sites)
