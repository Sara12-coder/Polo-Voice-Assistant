"""News headline retrieval using public RSS feeds."""
import feedparser

RSS_FEEDS = [
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.theguardian.com/world/rss",
]


def news(limit: int = 5):
    headlines = []
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                title = getattr(entry, "title", "").strip()
                if title and title not in headlines:
                    headlines.append(title)
                if len(headlines) >= limit:
                    return headlines
        except Exception as exc:
            print(f"News feed error: {exc}")
    if not headlines:
        return ["News could not be retrieved. Please check your internet connection."]
    return headlines
