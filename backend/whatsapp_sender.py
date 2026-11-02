import pyautogui
import time
import asyncio
from backend.app_open import open_app
from backend.speechtotext import Speech_To_Text_Python
from backend.TextToSpeech import speak


# FIX: Add TTS queue for non-blocking speech
tts_queue = asyncio.Queue()

async def tts_worker():
    while True:
        message = await tts_queue.get()
        try:
            await speak(message)
        except Exception as e:
            print("TTS Error:", e)
        tts_queue.task_done()


# WhatsApp Automation
async def whatsapp_message(name, message):
    open_app("whatsapp")
    time.sleep(5)

    time.sleep(1)
    pyautogui.hotkey("ctrl", "f")
    time.sleep(1)

    pyautogui.write(name, interval=0.05)
    time.sleep(1)

    pyautogui.press("enter")
    time.sleep(1)

    pyautogui.write(message, interval=0.05)
    time.sleep(1)

    pyautogui.press("enter")

    # FIX: Use TTS queue instead of await speak()
    await tts_queue.put("Message sent")


# Command Handler
async def handle_command(text):
    text = text.lower().strip()

    if not text:
        return

    # Remove all platform indicators completely
    text = text.replace("in whatsapp", "").replace("on whatsapp", "").strip()
    text = text.replace("  ", " ").strip()  # Remove extra spaces

    if "send" in text and " to " in text:
        try:
            # Parse "send [message] to [name]"
            # Remove send/message/msg keywords first
            text = text.replace("send", " ").replace("message", " ").replace("msg", " ").strip()
            text = text.replace("  ", " ").strip()  # Clean extra spaces
            
            # Now split by "to"
            if " to " in text:
                message, name = text.split(" to ", 1)
                message = message.strip()
                name = name.strip()
            else:
                raise ValueError("Missing 'to' in command")

            if not name or not message:
                raise ValueError("Name or message is empty")

            await whatsapp_message(name, message)

        except Exception as e:
            print("ERROR:", e)
            await tts_queue.put("I couldn't understand. Who should I message?")
            
            # Wait for TTS to finish before listening
            await asyncio.sleep(2)
            name = await asyncio.to_thread(Speech_To_Text_Python)

            await tts_queue.put("What should I say?")
            
            # Wait for TTS to finish before listening
            await asyncio.sleep(2)
            message = await asyncio.to_thread(Speech_To_Text_Python)

            await whatsapp_message(name, message)


# Main Loop
async def main():
    asyncio.create_task(tts_worker())
    
    while True:
        print("Listening...")
        # FIX: Use asyncio.to_thread() for blocking calls
        text = await asyncio.to_thread(Speech_To_Text_Python)

        if not text:
            continue

        print("You said:", text)
        await handle_command(text)


if __name__ == "__main__":
    asyncio.run(main())



