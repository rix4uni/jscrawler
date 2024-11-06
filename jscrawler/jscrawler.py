import sys
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import argparse
import urllib3

# Warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define the version
__version__ = "v0.0.2"  # Current Version of jscrawler

BANNER = rf"""
       _                                     __           
      (_)_____ _____ _____ ____ _ _      __ / /___   _____
     / // ___// ___// ___// __ `/| | /| / // // _ \ / ___/
    / /(__  )/ /__ / /   / /_/ / | |/ |/ // //  __// /    
 __/ //____/ \___//_/    \__,_/  |__/|__//_/ \___//_/     
/___/
                                            {__version__}
"""

def main():
    parser = argparse.ArgumentParser(description='jscrawler - Fetches JavaScript links from a list of URLs or live subdomains.')
    parser.add_argument('--timeout', default=5, help='Timeout (in seconds) for http client (default 5)')
    parser.add_argument('--complete', action='store_true', help='Get Complete URL (default false)')
    parser.add_argument('-o', '--output', help='Output file to save results')
    parser.add_argument('-v', '--verbose', action='store_true', help='Display info of what is going on')
    parser.add_argument('--silent', action='store_true', help='Run without printing the banner')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__, help='Show Current Version of jscrawler')
    args = parser.parse_args()

    # Print banner if not in silent mode
    if not args.silent:
        print(BANNER)

    for base_url in sys.stdin:
        base_url = base_url.rstrip()

        try:
            if args.verbose:
                print(f"Processing URL: {base_url}")
            response = requests.get(base_url, timeout=int(args.timeout), verify=False)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            if args.verbose:
                print(f"Timeout occurred while fetching: {base_url}")
            continue
        except requests.exceptions.SSLError:
            if args.verbose:
                print(f"SSL error occurred while fetching: {base_url}")
            continue
        except requests.exceptions.ConnectionError:
            if args.verbose:
                print(f"A connection error occurred. Please check your internet connection: {base_url}")
            continue
        except requests.exceptions.HTTPError as e:
            if args.verbose:
                print(f"HTTP Error {e.response.status_code}: {base_url}")
            continue
        except requests.exceptions.RequestException:
            if args.verbose:
                print(f"An error occurred: {base_url}")
            continue
        except KeyboardInterrupt:
            exit(0)

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
                    if not '.json' in full_url:
                        print(f"{full_url}")

                        if args.output:
                            with open(args.output, 'a') as file:
                                file.write(full_url + '\n')
                else:
                    if not '.json' in link:
                        print(f"{link}")

                        if args.output:
                            with open(args.output, 'a') as file:
                                file.write(link + '\n')

if __name__ == "__main__":
    main()