# CSPGenPro

A Python-based Content Security Policy (CSP) generator tool that crawls a given website, extracts all external domains, and saves the result to a file. It can handle deep website crawls up to a maximum specified depth and display real-time progress during the crawl. This tool is useful for building a robust CSP header by identifying all external resources used on a website.

features for crawling a website and generating a report with external domains, including options to specify the URL, maximum depth, timeout, and output file via command-line arguments.

### Features
- Crawls a website up to a user-defined depth.
- Extracts and lists external domains used (e.g., for scripts, images, iframes).
- Skips mailto: and data: URIs.
- Customizable timeout for web requests.
- Displays real-time progress, showing the current depth and URLs being fetched.
- Outputs results to a specified file.
- Command-line interface for easy usage.

### Installation
* Clone the repository:
```
git clone https://github.com/h4rithd/CSPGenPro/blob/master/cspgenpro.py
cd csp-generator
```
* Install dependencies: The script uses requests and beautifulsoup4 libraries. Install them using pip:
```
pip install requests beautifulsoup4
```

### Usage
The script takes several command-line arguments to configure the crawl, such as URL, depth, timeout, and output file.

#### Basic Usage
```
python3 cspgenpro.py -u https://example.com -o output.txt
```
This command will crawl https://example.com with the default maximum depth of 5 and timeout of 5 seconds, saving external domains to output.txt.

#### Full Usage Example
```
python3 cspgenpro.py -u https://example.com -o domains.txt -d 10 -t 10
```

* `-u` / `--url`: Required. The URL of the website to crawl.
* `-o` / `--output`: Required. The output file where the result will be saved.
* `-d` / `--depth`: Optional. The maximum depth to crawl (default is 5).
* `-t` / `--timeout`: Optional. The timeout for each request in seconds (default is 5).

### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Contribution

Feel free to submit issues, fork the repository, and make pull requests. All contributions are welcome!
