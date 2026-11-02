import string
import asyncio
from data.brain_input_cleanup import STOP_WORDS
from data.synonym_data import synonyms
from backend.handlers.messaging_handler import handle_messaging
from backend.handlers.web_handler import handle_web
from backend.handlers.music_handler import handle_music
from backend.handlers.search_handler import handle_search
from backend.llm_engine import ask_jarvis
from backend.TextToSpeech import speak


COMMAND_KEYWORDS = ["open", "play", "search", "send", "message"]


async def brain(query):
    """
    Main router for all Jarvis commands.
    """

    original_query = query
    input_text = query.lower()
    input_text = input_text.translate(str.maketrans('', '', string.punctuation))
    input_text = " ".join(word for word in input_text.split() if word not in STOP_WORDS)

    # Apply synonym replacements
    for phrase, replacement in synonyms.items():
        if phrase in input_text:
            input_text = input_text.replace(phrase, replacement)

    words = input_text.split()
    if not words:
        return

    # 🔥 Detect command anywhere in sentence
    detected_command = None
    for word in words:
        if word in COMMAND_KEYWORDS:
            detected_command = word
            break

    # =============================
    # ROUTING SECTION
    # =============================

    if detected_command in ["send", "message"]:
        return await handle_messaging(original_query)

    elif detected_command == "open":
        return await handle_web(original_query)

    elif detected_command == "play":
        return await handle_music(original_query)

    elif detected_command == "search":
        return await handle_search(original_query)

    # =============================
    # LLM FALLBACK (CHAT MODE)
    # =============================

    else:
        reply = ask_jarvis(original_query)
        await speak(reply)
        return reply