import atexit
import multiprocessing
import time
from concurrent.futures import ProcessPoolExecutor
from typing import List

import requests

session: requests.Session


def main():
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    download_all_sites(sites)


def download_all_sites(sites: List[str]):
    with ProcessPoolExecutor(initializer=init_process) as executor:
        executor.map(download_site, sites)


def download_site(url: str):
    with session.get(url) as response:
        name = multiprocessing.current_process().name
        print(f"{name}:Read {len(response.content)} bytes from {url}")


def init_process():
    global session
    session = requests.Session()
    atexit.register(session.close)
