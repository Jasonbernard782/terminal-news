import feedparser
from bs4 import BeautifulSoup


def clean_html(html: str) -> str:
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def fetch_feeds(feeds: dict):
    results = []

    for feed_name, url in feeds.items():
        feed = feedparser.parse(url)

        # Add a header for this feed
        results.append(
            {
                "type": "header",
                "title": feed_name,
            }
        )

        # Add articles
        for entry in feed.entries[:10]:
            results.append(
                {
                    "type": "article",
                    "feed": feed_name,
                    "title": entry.get("title", "No title"),
                    "link": entry.get("link", ""),
                    "summary": clean_html(entry.get("summary", "")),
                }
            )

    return results
