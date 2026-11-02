import os
import requests


class SerpAPISearch:
    def __init__(self, timeout=10):
        self.api_key = os.getenv("SERPAPI_KEY")
        if not self.api_key:
            raise ValueError("❌ SERPAPI_KEY not found in environment variables.")

        self.api_url = "https://serpapi.com/search"
        self.timeout = timeout

    def search(self, query, max_results=5):
        params = {
            "q": query,
            "engine": "google",
            "api_key": self.api_key,
            "num": max_results
        }

        try:
            response = requests.get(self.api_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            return {"error": str(e), "results": []}

        results = []

        for item in data.get("organic_results", []):
            results.append({
                "title": item.get("title"),
                "snippet": item.get("snippet"),
            })

        return {
            "query": query,
            "results": results[:max_results],
            "api_response_time": response.elapsed.total_seconds(),
            "raw": data  # Optional: remove later if not needed
        }


# ==========================
# 📝 Convert search result into a paragraph
# ==========================
def result_to_paragraph(result):
    title = result.get("title", "")
    snippet = result.get("snippet", "")
    
    # Don't include URLs - just title and snippet
    if title and snippet:
        paragraph = f"{title}. {snippet}"
    elif title:
        paragraph = f"{title}"
    else:
        paragraph = "No information available."
    return paragraph

def results_to_single_paragraph(results):
    if not results:
        return "No information found."
    
    combined = " ".join([result_to_paragraph(res) for res in results])
    return combined


