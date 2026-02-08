# core/config.py

DEFAULT_CONFIG = {
    "feeds": {
        # Hacker / Cybersecurity
        "Hacker News": "https://news.ycombinator.com/rss",
        "The Hacker News": "https://thehackernews.com/feeds/posts/default",
        "Krebs on Security": "https://krebsonsecurity.com/feed/",
        "Security Week": "https://feeds.feedburner.com/securityweek",
        "Bleeping Computer": "https://www.bleepingcomputer.com/feed/",
        "Mozilla Security Blog": "https://blog.mozilla.org/security/feed/",
        "Ars Technica": "http://feeds.arstechnica.com/arstechnica/index",
        # General news
        "Sky News": "https://feeds.skynews.com/feeds/rss/home.xml",
        "BBC News": "http://feeds.bbci.co.uk/news/rss.xml",
    }
}


def load_config():
    return DEFAULT_CONFIG
