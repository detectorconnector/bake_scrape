import requests
from bs4 import BeautifulSoup
import re
import time

def find_local_businesses(town, max_results=5):
    search_query = f"{town} local businesses site:.com"
    search_url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(search_query)}"

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            match = re.search(r'(https?://[^&]+)', href)
            if match:
                url = match.group(1)
                if url not in links:
                    links.append(url)
            if len(links) >= max_results:
                break

        time.sleep(1)  # Be polite
        return links
    except Exception as e:
        print(f"[ERROR] Failed to search for businesses in {town}: {e}")
        return []
