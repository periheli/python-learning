import time

import requests


def main():
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    download_all_sites(sites)


def download_all_sites(sites):
    with requests.Session() as session:
        for url in sites:
            download_site(url, session)


def download_site(url, session):
    with session.get(url) as response:
        print(f"Read {len(response.content)} bytes from {url}")
