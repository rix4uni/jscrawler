import sys
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import argparse
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed

# Warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define the version
__version__ = "v0.0.3"  # Current Version of jscrawler

BANNER = rf"""
       _                                     __           
      (_)_____ _____ _____ ____ _ _      __ / /___   _____
     / // ___// ___// ___// __ `/| | /| / // // _ \ / ___/
    / /(__  )/ /__ / /   / /_/ / | |/ |/ // //  __// /    
 __/ //____/ \___//_/    \__,_/  |__/|__//_/ \___//_/     
/___/
                                            {__version__}
"""

def save_output(output_file, url):
    """Save the URL to the output file if specified."""
    if output_file:
        with open(output_file, 'a') as file:
            file.write(url + '\n')

def extract_js_links(base_url, html, complete, output_file, verbose):
    """Extract JavaScript links from HTML using regex and script tag parsing."""
    soup = BeautifulSoup(html, 'html.parser')
    js_links = set()

    # Extract links using regex
    soup_str = str(soup)
    regex_links = re.findall(r"['\"]([^'\"]*\.js[^'\"]*)['\"]", soup_str)
    for link in regex_links:
        link = link.strip('\'"')
        if complete:
            full_url = urljoin(base_url, link)
            if '.json' not in full_url:
                js_links.add(full_url)
        else:
            if '.json' not in link:
                js_links.add(link)

    # Extract script src attributes with type="text/javascript"
    for script in soup.find_all('script', src=True):
        script_type = script.get('type', '').lower()
        if script_type == 'text/javascript' or not script_type:
            src_link = script['src']
            if complete:
                full_url = urljoin(base_url, src_link)
                js_links.add(full_url)
            else:
                js_links.add(src_link)

    # Output the collected links
    for js_link in js_links:
        print(js_link)
        save_output(output_file, js_link)

def process_url(base_url, timeout, complete, output_file, verbose):
    """Fetch and process a single URL."""
    base_url = base_url.strip()
    try:
        if verbose:
            print(f"Processing URL: {base_url}")
        response = requests.get(base_url, timeout=timeout, verify=False)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        if verbose:
            print(f"Timeout occurred while fetching: {base_url}")
    except requests.exceptions.SSLError:
        if verbose:
            print(f"SSL error occurred while fetching: {base_url}")
    except requests.exceptions.ConnectionError:
        if verbose:
            print(f"A connection error occurred. Please check your internet connection: {base_url}")
    except requests.exceptions.HTTPError as e:
        if verbose:
            print(f"HTTP Error {e.response.status_code}: {base_url}")
    except requests.exceptions.RequestException as e:
        if verbose:
            print(f"An error occurred: {e}")
    except KeyboardInterrupt:
        exit(0)
    else:
        extract_js_links(base_url, response.text, complete, output_file, verbose)

def main():
    parser = argparse.ArgumentParser(description='jscrawler - Fetches JavaScript links from a list of URLs or live subdomains.')
    parser.add_argument('--timeout', default=15, type=int, help='Timeout (in seconds) for http client (default 15)')
    parser.add_argument('--complete', action='store_true', help='Get Complete URL (default false)')
    parser.add_argument('-o', '--output', help='Output file to save results')
    parser.add_argument('-v', '--verbose', action='store_true', help='Display info of what is going on')
    parser.add_argument('--silent', action='store_true', help='Run without printing the banner')
    parser.add_argument('-t', '--threads', default=50, type=int, help='Number of threads to use (default 50)')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__, help='Show Current Version of jscrawler')
    args = parser.parse_args()

    # Print banner if not in silent mode
    if not args.silent:
        print(BANNER)

    urls = [url.strip() for url in sys.stdin if url.strip()]

    # Process URLs using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [executor.submit(process_url, url, args.timeout, args.complete, args.output, args.verbose) for url in urls]
        
        try:
            for future in as_completed(futures):
                future.result()  # This will raise exceptions if any occurred during processing
        except KeyboardInterrupt:
            print("Interrupted by user. Shutting down...")
            executor.shutdown(wait=False)

if __name__ == "__main__":
    main()
