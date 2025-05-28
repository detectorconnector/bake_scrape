# app.py
from flask import Flask, render_template, request
from utils.scraper import scrape_website
from utils.ai_prompt import generate_outreach

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    if request.method == 'POST':
        url = request.form['url']
        scraped_text = scrape_website(url)
        outreach = generate_outreach(scraped_text)
        result = {
            'url': url,
            'scraped': scraped_text,
            'ideas': outreach['ideas'],
            'questions': outreach['questions'],
            'opener': outreach['opener']
        }
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
