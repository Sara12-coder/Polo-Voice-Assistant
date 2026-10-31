"""Browser-based Google search helper for Polo."""
import urllib.parse
import webbrowser


class sear:
    def get_infoo(self, query: str) -> None:
        if not query or not query.strip():
            print("No search query provided.")
            return
        url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(query.strip())
        webbrowser.open(url)
        print(f"Opened Google search results for: {query}")
