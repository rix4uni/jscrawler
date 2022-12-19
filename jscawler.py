import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import concurrent.futures

def crawl_js_links(url):
    parsed_url = urlparse(url)

    # The domain name is the netloc attribute of the parsed URL
    domain_name = parsed_url.netloc

    # Make a request to the website
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all the script tags
    script_tags = soup.find_all('script')
    # Iterate over the script tags
    for tag in script_tags:
        # Check if the tag has a src attribute
        if 'src' in tag.attrs:
            # Get the link from the src attribute
            link = tag['src']
            # Check if the link ends with .js
            if re.search('.js',link):
                # If the link starts with a dual //
                if link.startswith('//'):
                    link = 'https:' + link
                # If the link starts with a single /
                elif link.startswith('/'):
                    link = 'https://' + domain_name + link
                # If the link starts with a \/\/ remove all backslashes
                elif link.startswith('\\'):
                    link = 'https:' + link.replace("\\", "")
                # Print the link
                print(link)
# Open the file and read the URLs
with open(sys.argv[1], 'r') as f:
    lines = f.readlines()
    # Create a thread pool with 50 threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        # Iterate over the URLs
        for url in lines:
            url = url.strip()
            # Submit the task to the thread pool
            executor.submit(crawl_js_links, url)