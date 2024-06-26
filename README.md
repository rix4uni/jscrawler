# jscrawler

## Installation
```
git clone https://github.com/rix4uni/jscrawler.git
cd jscrawler
pip3 install -r requirements.txt
```

## Usage
```
usage: jscrawler.py [-h] [--timeout TIMEOUT] [--complete] [-o OUTPUT] [-v] [-nc] [--silent] [--version]

jscrawler - Fetches JavaScript links from a list of URLs or live subdomains.

options:
  -h, --help            show this help message and exit
  --timeout TIMEOUT     Timeout (in seconds) for http client (default 5)
  --complete            Get Complete URL (default false)
  -o OUTPUT, --output OUTPUT
                        Output file to save results
  -v, --verbose         Display info of what is going on
  -nc, --no-color       Print without ANSI color codes
  --silent              Run without printing the banner
  --version             Show Current Version of jscrawler
```

## Example usages

Single URLs:
```
echo "https://www.dell.com" | python3 jscrawler.py
```

Multiple URLs:
```
cat live-subs.txt | python3 jscrawler.py
```
