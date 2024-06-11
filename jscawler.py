import sys
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

for base_url in sys.stdin:
	base_url = base_url.rstrip()

	response = requests.get(base_url, timeout=5, verify=False)
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
	        # Convert relative URLs to absolute URLs
	        full_url = urljoin(base_url, link)
	        print(full_url)
