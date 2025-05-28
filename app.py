# app.py
import os
import json
from flask import Flask, render_template, request
from utils.scraper import scrape_website
from utils.ai_prompt import generate_outreach
from utils.local_search import find_local_businesses

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    if request.method == 'POST':
        town = request.form.get('town')
        url = request.form.get('url')

        if town:
            # Town mode: find businesses and run batch scrape
            business_urls = find_local_businesses(town)
            batch_results = []
            for biz_url in business_urls:
                scraped_text = scrape_website(biz_url)
                outreach = generate_outreach(scraped_text)
                batch_results.append({
                    'url': biz_url,
                    'scraped': scraped_text,
                    'ideas': outreach['ideas'],
                    'questions': outreach['questions'],
                    'opener': outreach['opener']
                })
            result['batch'] = batch_results
        elif url:
            # Manual URL mode
            scraped_text = scrape_website(url)
            outreach = generate_outreach(scraped_text)
            result = {
                'url': url,
                'scraped': scraped_text,
                'ideas': outreach['ideas'],
                'questions': outreach['questions'],
                'opener': outreach['opener']
            }

    # Load overnight batch results from file if available
    try:
        with open("data/last_batch.json") as f:
            result['overnight'] = json.load(f)
    except Exception:
        result['overnight'] = []

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
