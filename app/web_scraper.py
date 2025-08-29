import requests
from bs4 import BeautifulSoup
import os

def scrape_site(start_url, max_pages=10):
    visited = set()
    to_visit = [start_url]
    content = {}

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop()
        if url in visited or not url.startswith(start_url):
            continue
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            text = soup.get_text(separator="\n", strip=True)
            content[url] = text
            visited.add(url)

            for a in soup.find_all('a', href=True):
                link = a['href']
                if link.startswith('/'):
                    link = start_url.rstrip('/') + link
                if link.startswith(start_url) and link not in visited:
                    to_visit.append(link)
        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")
    return content
