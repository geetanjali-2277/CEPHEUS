import requests

class DuckDuckGoSearch:
    def __init__(self, timeout=10):
        self.api_url = "https://api.duckduckgo.com/"
        self.timeout = timeout

    def search(self, query, max_results=5):
        params = {
            "q": query,
            "format": "json",
            "no_redirect": 1,
            "no_html": 1,
            "skip_disambig": 1
        }

        try:
            response = requests.get(self.api_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            return {"error": str(e), "results": []}

        results = []

        # Instant answer
        if data.get("AbstractText"):
            results.append({
                "title": data.get("Heading", "Result"),
                "snippet": data.get("AbstractText"),
                "url": data.get("AbstractURL", "")
            })

        # Related topics (including nested)
        for topic in data.get("RelatedTopics", []):
            if isinstance(topic, dict) and "Text" in topic:
                results.append({
                    "title": topic.get("Text", "").split(" - ")[0],
                    "snippet": topic.get("Text", ""),
                    "url": topic.get("FirstURL", "")
                })

            if isinstance(topic, dict) and "Topics" in topic:
                for sub in topic["Topics"]:
                    if "Text" in sub:
                        results.append({
                            "title": sub.get("Text", "").split(" - ")[0],
                            "snippet": sub.get("Text", "")
                        })

        return {
            "query": query,
            "results": results[:max_results],
            "api_response_time": response.elapsed.total_seconds()
        }


