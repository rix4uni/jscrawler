## jscrawler

Fetches javascript file from a list of URLS or subdomains.

## Installation
```
git clone https://github.com/rix4uni/jscrawler.git
cd jscrawler
python3 setup.py install
```

## Usage
```
usage: jscrawler [-h] [--timeout TIMEOUT] [--complete] [-o OUTPUT] [-v] [-nc] [--silent] [--version]

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
echo "https://www.dell.com" | jscrawler
```

Multiple URLs:
```
cat live-subs.txt | jscrawler
```
