"""YouTube search helper for Polo. Opens results in the default browser."""
import urllib.parse
import webbrowser


class music:
    def play(self, query: str) -> None:
        if not query or not query.strip():
            print("Please provide a video title.")
            return
        url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(query.strip())
        webbrowser.open(url)
        print(f"Opened YouTube search results for: {query}")
