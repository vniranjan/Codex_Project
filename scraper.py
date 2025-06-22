import hashlib
import sqlite3
from datetime import datetime
from typing import List

import feedparser
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from rss_sources import RSS_FEEDS

DB_PATH = "articles.db"
LANGUAGE = "english"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS articles (
            id TEXT PRIMARY KEY,
            title TEXT,
            link TEXT,
            summary TEXT,
            published TEXT,
            upvotes INTEGER DEFAULT 0,
            downvotes INTEGER DEFAULT 0
        )
        """
    )
    conn.commit()
    conn.close()


def summarize(text: str, sentence_count: int = 3) -> str:
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = LsaSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    sentences = summarizer(parser.document, sentence_count)
    return " ".join(str(s) for s in sentences)


def fetch_articles() -> List[dict]:
    items = []
    for feed_url in RSS_FEEDS:
        d = feedparser.parse(feed_url)
        for entry in d.entries:
            item_id = hashlib.sha256(entry.link.encode()).hexdigest()
            items.append(
                {
                    "id": item_id,
                    "title": entry.title,
                    "link": entry.link,
                    "summary": entry.summary if hasattr(entry, "summary") else "",
                    "published": entry.get("published", datetime.utcnow().isoformat()),
                }
            )
    return items


def store_articles(items: List[dict]):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for item in items:
        try:
            c.execute(
                "INSERT INTO articles (id, title, link, summary, published) VALUES (?, ?, ?, ?, ?)",
                (item["id"], item["title"], item["link"], summarize(item["summary"]), item["published"],),
            )
        except sqlite3.IntegrityError:
            # already exists
            pass
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    items = fetch_articles()
    store_articles(items)
    print(f"Stored {len(items)} articles")
