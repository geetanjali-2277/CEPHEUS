import asyncio
from backend.whatsapp_sender import handle_command as handle_whatsapp
from backend.telegram_messenger import handle_command as handle_telegram
from backend.TextToSpeech import speak


async def handle_messaging(query):
    """
    Route messaging commands to Telegram or WhatsApp.
    """
    query_lower = query.lower()

    try:
        # Detect platform
        if "telegram" in query_lower:
            print("Routing to Telegram Messenger")
            await handle_telegram(query)
            msg = "Message sent via Telegram."        
            return msg                                 

        elif "whatsapp" in query_lower:
            print("Routing to WhatsApp Messenger")
            await handle_whatsapp(query)
            msg = "Message sent via WhatsApp."        
            return msg                                 

        else:
            # Default to WhatsApp if no platform specified
            print("Routing to default WhatsApp Messenger")
            await handle_whatsapp(query)
            msg = "Message sent via WhatsApp."        
            return msg                               

    except Exception as e:
        print(f"Messaging Error: {e}")
        msg = "Sorry, I couldn't process the message." 
        await speak(msg)
        return msg                                      
