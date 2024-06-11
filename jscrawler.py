import sys
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import argparse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define the version
__version__ = "v0.0.1"  # Current Version of jscrawler

parser = argparse.ArgumentParser(description='jscrawler - Fetches JavaScript links from a list of URLs or live subdomains.')
parser.add_argument('--timeout', default=5, help='Timeout (in seconds) for http client (default 15)')
parser.add_argument('--complete', action='store_true', help='Get Complete URL (default false)')
parser.add_argument('-o', '--output', help='Output file to save results')
parser.add_argument('-v', '--verbose', action='store_true', help='Display info of what is going on')
parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
args = parser.parse_args()

for base_url in sys.stdin:
    base_url = base_url.rstrip()

    try:
        response = requests.get(base_url, timeout=int(args.timeout), verify=False)
        if args.verbose:
            print(f"Processing URL: {base_url}")
    except requests.exceptions.Timeout:
        if args.verbose:
            print(f"Timeout occurred while fetching: {base_url}")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')

    # # Convert the BeautifulSoup object to a string
    soup_str = str(soup)

    # # Use the regex pattern to find all matches
    links = re.findall(r"['\"]([^'\"]*\.js[^'\"]*)['\"]", soup_str)

    # Filter and print only those links that contain .js
    for link in links:
        if '.js' in link:
            # Remove surrounding quotes
            link = link.strip('\'"')

            if args.complete:
                # Convert relative URLs to absolute URLs
                full_url = urljoin(base_url, link)
                print(full_url)

                if args.output:
                    with open(args.output, 'a') as file:
                        file.write(full_url + '\n')
            else:
                print(link)

                if args.output:
                    with open(args.output, 'a') as file:
                        file.write(link + '\n')
