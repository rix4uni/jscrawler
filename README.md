## jscrawler

Fetches javascript file from a list of URLS or subdomains.

## Installation
```
git clone https://github.com/rix4uni/jscrawler.git
cd jscrawler
python3 setup.py install
```

## pip
```
pip install jscrawler
```

## pipx
Quick setup in isolated python environment using [pipx](https://pypa.github.io/pipx/)
```
pipx install --force git+https://github.com/rix4uni/jscrawler.git
```

## Usage
```
usage: jscrawler [-h] [--timeout TIMEOUT] [--complete] [-o OUTPUT] [-v] [--silent] [-t THREADS] [--version]

jscrawler - Fetches JavaScript links from a list of URLs or live subdomains.

options:
  -h, --help            show this help message and exit
  --timeout TIMEOUT     Timeout (in seconds) for http client (default 15)
  --complete            Get Complete URL (default false)
  -o OUTPUT, --output OUTPUT
                        Output file to save results
  -v, --verbose         Display info of what is going on
  --silent              Run without printing the banner
  -t THREADS, --threads THREADS
                        Number of threads to use (default 50)
  --version             Show Current Version of jscrawler
```

## Example usages

Single URLs:
```
echo "https://www.dell.com" | jscrawler
```

Multiple URLs:
```
cat alive_subs.txt | jscrawler
```

## Comparison
```
▶ echo "https://www.dell.com" | getJS --complete | wc -l
3

▶ echo "https://www.dell.com" | subjs | wc -l
3

▶ echo "https://www.dell.com" | jscrawler --silent --complete | wc -l
12
```