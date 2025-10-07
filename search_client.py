# search_client.py
import os
import requests

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

def search_web(query, num=1):
    """
    Use Google Custom Search if keys are present.
    Otherwise use DuckDuckGo instant answer API (limited).
    Returns a short snippet string.
    """
    if GOOGLE_API_KEY and GOOGLE_CSE_ID:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {"key": GOOGLE_API_KEY, "cx": GOOGLE_CSE_ID, "q": query, "num": num}
        r = requests.get(url, params=params, timeout=6)
        r.raise_for_status()
        data = r.json()
        items = data.get("items")
        if items:
            return items[0].get("snippet") or items[0].get("title")
        return None
    # DuckDuckGo fallback
    dd = requests.get("https://api.duckduckgo.com", params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}, timeout=6)
    dd.raise_for_status()
    j = dd.json()
    if j.get("AbstractText"):
        return j.get("AbstractText")
    # try related topics
    related = j.get("RelatedTopics")
    if related:
        first = related[0]
        if isinstance(first, dict) and first.get("Text"):
            return first.get("Text")
    return None
