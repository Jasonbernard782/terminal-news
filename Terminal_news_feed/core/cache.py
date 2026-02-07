import json
from pathlib import Path

CACHE_FILE = Path.home() / ".terminal_news_cache.json"


def save_cache(items: list):
    try:
        CACHE_FILE.write_text(json.dumps(items))
    except Exception:
        pass


def load_cache() -> list:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text())
        except Exception:
            pass
    return []
