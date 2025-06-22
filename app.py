from flask import Flask, render_template, request, redirect, url_for
import sqlite3

DB_PATH = "articles.db"

app = Flask(__name__)


def get_articles():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT id, title, link, summary, upvotes, downvotes FROM articles ORDER BY upvotes - downvotes DESC, published DESC LIMIT 50"
    )
    articles = [
        {
            "id": row[0],
            "title": row[1],
            "link": row[2],
            "summary": row[3],
            "upvotes": row[4],
            "downvotes": row[5],
        }
        for row in c.fetchall()
    ]
    conn.close()
    return articles


@app.route("/")
def index():
    articles = get_articles()
    return render_template("index.html", articles=articles)


@app.route("/vote/<article_id>/<vote_type>")
def vote(article_id: str, vote_type: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if vote_type == "up":
        c.execute("UPDATE articles SET upvotes = upvotes + 1 WHERE id = ?", (article_id,))
    elif vote_type == "down":
        c.execute("UPDATE articles SET downvotes = downvotes + 1 WHERE id = ?", (article_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
