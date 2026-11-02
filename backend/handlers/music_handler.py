from backend.music_player_youtube import play_music_on_youtube
from backend.music_player_spotify import play_music_on_spotify
from backend.TextToSpeech import speak
import asyncio


async def handle_music(query):
    """
    Route music commands to YouTube or Spotify.
    
    Examples:
    - "play song name on youtube"
    - "play song name on spotify"
    - "play song name" (defaults to YouTube)
    """
    query_lower = query.lower()
    
    try:
        # Remove "play" from query
        target = query_lower.replace("play", "").strip()
        
        if not target:
            msg = "I didn't understand what to play."   # 🔹 CHANGE 2
            await speak(msg)
            return msg
        
        # Detect platform
        platform = "youtube" if "youtube" in target else "spotify" if "spotify" in target else None
        
        # Remove platform mentions from song name
        target = (
            target
            .replace("on youtube", "")
            .replace("on spotify", "")
            .replace("youtube", "")
            .replace("spotify", "")
            .strip()
        )
        
        if platform == "youtube":
            print("Routing to YouTube Music Player")
            play_music_on_youtube(target)
            msg = f"Playing '{target}' on YouTube."
            await speak(msg)
            return msg
        elif platform == "spotify":
            print("Routing to Spotify Music Player")
            play_music_on_spotify(target)
            msg = f"Playing '{target}' on Spotify."
            await speak(msg)  
            return msg
        else:
            # Default to YouTube if no platform specified
            print("Routing to default YouTube Music Player")
            play_music_on_youtube(target)
            msg = f"Playing '{target}' on YouTube."
            await speak(msg)
            return msg
            
    except Exception as e:
        print(f"Music Handler Error: {e}")
        msg = "Sorry, I couldn't play that song."      
        await speak(msg)
        return msg
