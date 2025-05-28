# batch_scrape.py
import os, json
from utils.scraper import scrape_website
from utils.ai_prompt import generate_outreach
from utils.local_search import find_local_businesses

def main():
    town = "Owatonna, MN"
    print(f"[▶] Auto scraping for: {town}")
    urls = find_local_businesses(town, max_results=10)

    results = []
    for url in urls:
        print(f"[🔎] Processing: {url}")
        scraped = scrape_website(url)
        outreach = generate_outreach(scraped)
        results.append({
            "url": url,
            "scraped": scraped,
            "ideas": outreach["ideas"],
            "questions": outreach["questions"],
            "opener": outreach["opener"]
        })

    os.makedirs("data", exist_ok=True)
    with open("data/last_batch.json", "w") as f:
        json.dump(results, f, indent=2)
    print("[✔] Batch saved to data/last_batch.json")

if __name__ == "__main__":
    main()
