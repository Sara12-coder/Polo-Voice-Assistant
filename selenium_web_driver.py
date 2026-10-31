"""Wikipedia information helper.

The original project called this module through inforr().get_info(topic).
This reconstruction uses the Wikipedia REST API via requests, avoiding a
browser-driver installation. Internet access is required.
"""
import requests
import urllib.parse


class inforr:
    def get_info(self, topic: str) -> str:
        if not topic:
            print("No topic provided.")
            return ""
        title = urllib.parse.quote(topic.strip().replace(" ", "_"), safe="")
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
        try:
            response = requests.get(
                url,
                headers={"User-Agent": "PoloVoiceAssistant/1.0 (educational project)"},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            summary = data.get("extract", "No summary was available for that topic.")
            print(summary)
            return summary
        except requests.RequestException as exc:
            message = f"Could not retrieve Wikipedia information: {exc}"
            print(message)
            return message
