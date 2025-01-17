import random
import requests
from urllib import parse as urlparse

from plugins.banner import *

# User agents
defaultUserAgent = {'User-Agent': 's4sscanner ()', 'Accept': '*/*'}
timeout = 4

# Generate Random Strings
def generateRandomString(length=7):
    return ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for i in range(length))

# Parse URL
def parseUniformResourceLocatorFunc(url):
    url = url.replace('#', '%23')
    url = url.replace(' ', '%20')

    if ('://' not in url):
        url = f"http://{url}"
    scheme = urlparse.urlparse(url).scheme
    pathofFile = urlparse.urlparse(url).path
    if pathofFile == '':
        pathofFile = '/'

    return {
        "scheme": scheme,
        "site": f"{scheme}://{urlparse.urlparse(url).netloc}",
        "host": urlparse.urlparse(url).netloc.split(":")[0],
        "pathofFile": pathofFile
    }

# Set URL path
def setUniformResourceLocatorPathFuc(url, path="/"):
    url_parsed = parseUniformResourceLocatorFunc(url)
    return f'{url_parsed["site"]}{path}'

# Verify Base Requests
def verifyBaseRequestsFunc(url, method):
    r = requests.request(url=url, method=method, headers=defaultUserAgent, verify=False, timeout=timeout)
    return r.status_code

# Test URL for CVE
def testUniformResourceLocatorCVE(url):
    mainPayloadVar = "class.module.classLoader[{{random}}]={{random}}"
    mainPayloadVar = mainPayloadVar.replace("{{random}}", generateRandomString())
    payloads = [mainPayloadVar]
    
    for payload in payloads:
        parameter, value = payload.split("=")
        if "POST" in ("POST", "ALL"):
            try:
                requestVar = requests.request(url=url, method="POST", headers=defaultUserAgent,
                                              verify=False, timeout=timeout, data={parameter: value})
                if requestVar.status_code not in (200, 404) and verifyBaseRequestsFunc(url, "POST") != requestVar.status_code:
                    return True
            except Exception as error:
                print(f"Found an Error : {error}")
        if "GET" in ("GET", "ALL"):
            try:
                r = requests.request(url=url, method="GET", headers=defaultUserAgent,
                                     verify=False, timeout=timeout, params={parameter: value})
                if r.status_code not in (200, 404) and verifyBaseRequestsFunc(url, "GET") != r.status_code:
                    return True
            except Exception as error:
                print(f"Found an Error : {error}")
    return False

# Main RCE scanning function
def start_rce_scan(url):
    urls = [url]
    vulnerableHosts = []
    for url in urls:
        result = testUniformResourceLocatorCVE(url)
        if result:
            vulnerableHosts.append(url)
    
    return vulnerableHosts

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python rce_scanning.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    results = start_rce_scan(url)
    print(results)
