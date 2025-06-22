# AI News Aggregator

This project is a small Flask application that aggregates AI-related news articles from several technology websites using their RSS feeds. Articles are summarized and ranked by community feedback.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Initialize the database and fetch articles:
   ```bash
   python scraper.py
   ```
3. Run the web server:
   ```bash
   python app.py
   ```
4. Open your browser at `http://localhost:5000`.

## Adding RSS Sources

Edit `rss_sources.py` to add or remove RSS feed URLs.
