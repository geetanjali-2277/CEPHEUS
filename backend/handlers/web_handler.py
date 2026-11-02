from backend.app_open import open_app
from backend.web_open import open_web
from data.web_data import websites
from backend.TextToSpeech import speak
import asyncio


websites_lower = {k.lower(): v for k, v in websites.items()}


async def handle_web(query):
    """
    Route open commands to apps or websites.
    """
    query_lower = query.lower()
    
    try:
        # Remove "open" from query
        target = query_lower.replace("open", "").strip()
        
        if not target:
            msg="I didn't understand what to open."
            await speak(msg)
            return msg
        
        # Check if it's a website
        if target in websites_lower:
            print("Routing to WEB")
            open_web(target)
            msg = f"Opening {target} website."
            await speak(msg)
            return msg
        else:
            print("Routing to APP")
            msg = f"Opening {target} app."
            await speak(msg)
            open_app(target)
            return msg
            
    except Exception as e:
        print(f"Web Handler Error: {e}")
        msg = "Sorry, I couldn't open that."
        await speak(msg)
        return msg
