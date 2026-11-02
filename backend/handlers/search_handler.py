from backend.webquery_api import DuckDuckGoSearch
from backend.webquery_serp import SerpAPISearch, results_to_single_paragraph
from backend.TextToSpeech import speak


# Initialize search engines
duckduckgo_search = DuckDuckGoSearch(timeout=10)


async def handle_search(query):
    """
    Route search commands to available search APIs.
    Combines results from both SerpAPI and DuckDuckGo for comprehensive search.
    """
    query_lower = query.lower()

    try:
        # 🔹 CHANGE 1: replace only first "search"
        search_term = query_lower.replace("search", "", 1).strip()

        if not search_term:
            msg = "I didn't understand what to search."   
            await speak(msg)
            return msg                                     

        all_results = []

        # Try SerpAPI first
        try:
            print("Attempting SerpAPI search...")
            serp = SerpAPISearch(timeout=10)
            results = serp.search(search_term, max_results=3)

            if results.get("results"):
                print("SerpAPI Results found")
                all_results.extend(results["results"])
        except Exception as e:
            print(f"SerpAPI failed: {e}, falling back to DuckDuckGo...")

        # DuckDuckGo
        try:
            print("Using DuckDuckGo search...")
            results = duckduckgo_search.search(search_term, max_results=3)

            if results.get("results"):
                print("DuckDuckGo Results found")
                all_results.extend(results["results"])
        except Exception as e:
            print(f"DuckDuckGo failed: {e}")

        # Format and speak combined results
        if all_results:
            seen = set()
            unique_results = []

            for result in all_results:
                title = result.get("title", "")
                if title not in seen:
                    seen.add(title)
                    unique_results.append(result)

            formatted_text = results_to_single_paragraph(unique_results[:5])

            print("\n" + "="*50)
            print(formatted_text)
            print("="*50 + "\n")

            await speak(formatted_text)
            return formatted_text          

        else:
            msg = "Sorry, I couldn't find any results."   
            await speak(msg)
            return msg                                    

    except Exception as e:
        print(f"Search Handler Error: {e}")
        msg = "Sorry, I couldn't perform that search."   
        await speak(msg)
        return msg                                       
