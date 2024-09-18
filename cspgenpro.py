import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re
import sys
import warnings
from bs4 import XMLParsedAsHTMLWarning

# Suppress the XMLParsedAsHTMLWarning
warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)

# Set to avoid revisiting the same URLs
visited_urls = set()
external_domains = set()

# Banner
def print_banner():
    banner = """
-------------------------------------------------------------
------------------- | CSP Generator |------------------------
-------------------------------------------------------------
   _____  _____ _____   _____            _____           
  / ____|/ ____|  __ \\ / ____|          |  __ \\          
 | |    | (___ | |__) | |  __  ___ _ __ | |__) | __ ___  
 | |     \\___ \\|  ___/| | |_ |/ _ \\ '_ \\|  ___/ '__/ _ \\ 
 | |____ ____) | |    | |__| |  __/ | | | |   | | | (_) |
  \\_____|_____/|_|     \\_____|\\___|_| |_|_|   |_|  \\___/ 
                                                         
                                        by h4rith.com
-------------------------------------------------------------
    """
    print(banner)

# Function to determine if a URL is external
def is_external(url, base_domain):
    parsed_url = urlparse(url)
    return parsed_url.netloc and parsed_url.netloc != base_domain

# Function to crawl and collect external domains
def collect_external_domains(base_url, max_depth, timeout, output_file):
    def crawl(url, depth):
        if depth > max_depth or url in visited_urls:
            return

        visited_urls.add(url)

        # Skip mailto: links and data: URIs
        if url.startswith('mailto:') or url.startswith('data:'):
            return

        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code != 200:
                return
        except requests.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
            return

        base_domain = urlparse(base_url).netloc
        soup = BeautifulSoup(response.text, 'html.parser')

        print(f"[+] Depth {depth}: Fetched {url}")

        # Find all links, images, scripts, etc.
        tags = soup.find_all(['a', 'link', 'script', 'img', 'iframe'])
        for tag in tags:
            src_or_href = tag.get('href') or tag.get('src')
            if src_or_href:
                resource_url = urljoin(url, src_or_href)

                # Check if the resource is external
                if is_external(resource_url, base_domain):
                    external_domains.add(urlparse(resource_url).netloc)

                # Crawl only if it's an internal link and within depth
                elif not is_external(resource_url, base_domain):
                    crawl(resource_url, depth + 1)

    # Start crawling from the base URL
    crawl(base_url, 0)

    # Save output to file
    with open(output_file, 'w') as f:
        f.write("External domains found:\n")
        for domain in external_domains:
            f.write(f"{domain}\n")
    print(f"\n[+] Results saved to {output_file}")


# Main function to handle command line arguments and execute the script
if __name__ == "__main__":
    print_banner()

    # Argument parser
    parser = argparse.ArgumentParser(description='CSP Generator by h4rith.com')

    # Required arguments
    parser.add_argument('-u', '--url', required=True, help='URL to crawl')
    parser.add_argument('-o', '--output', required=True, help='Output file name')

    # Optional arguments
    parser.add_argument('-d', '--depth', type=int, default=5, help='Max depth to crawl (default: 5)')
    parser.add_argument('-t', '--timeout', type=int, default=5, help='Timeout in seconds (default: 5)')

    args = parser.parse_args()

    # Validate URL format
    if not re.match(r'https?://', args.url):
        print("Please enter a valid URL starting with http:// or https://")
        sys.exit(1)

    # Start crawling
    print(f"[!] Starting crawl on {args.url} with max depth {args.depth} and timeout {args.timeout}s\n")
    collect_external_domains(args.url, args.depth, args.timeout, args.output)

    print("\n------------------ Script from h4rithd.com ------------------")
