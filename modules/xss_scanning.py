import argparse
import requests
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
from random import randint
import warnings

from lib.helper.helper import *
from lib.helper.Log import *
from lib.core import core
from lib.crawler.crawler import *

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

epilog = """
Version: 0.5 Final
"""

def check(getopt):
    payload = int(getopt.payload_level)
    if payload > 6 and getopt.payload is None:
        Log.info("Do you want to use a custom payload (Y/n)?")
        answer = input("> " + W) 
        if answer.lower().strip() == "y":
            Log.info("Write the XSS payload below")
            payload = input("> " + W)
        else:
            payload = core.generate(randint(1, 6))
    else:
        payload = core.generate(payload)
    
    return payload if getopt.payload is None else getopt.payload

def parse_html(text):
    if text:
        return BeautifulSoup(text, "html.parser")
    return None

def get_body(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error connecting to {url}: {e}")
        return ""

def start_xss_scan(target_url, depth=2, payload_level=6, method=2, user_agent=agent, proxy=None, cookie='{"ID":"1094200543"}'):
    getopt = argparse.Namespace(
        u=target_url,
        depth=depth,
        payload_level=payload_level,
        payload=None,
        method=method,
        user_agent=user_agent,
        single=None,
        proxy=proxy,
        about=False,
        cookie=cookie
    )

    print(logo)
    Log.info("Starting XSS Scan...")

    if getopt.u:
        with open("xss.txt", "w") as file:
            file.write("")
        print("file cleared!")    
        core.main(getopt.u, getopt.proxy, getopt.user_agent, check(getopt), getopt.cookie, getopt.method)
        crawler.crawl(getopt.u, int(getopt.depth), getopt.proxy, getopt.user_agent, check(getopt), getopt.method, getopt.cookie)
    elif getopt.single:
        core.main(getopt.single, getopt.proxy, getopt.user_agent, check(getopt), getopt.cookie, getopt.method)
    elif getopt.about:
        print(epilog)

    with open("xss.txt", "r") as file:
        xss_results = file.read()

    return xss_results