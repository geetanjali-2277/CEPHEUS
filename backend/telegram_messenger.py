import pyautogui
import time
import asyncio
from backend.app_open import open_app
from backend.speechtotext import Speech_To_Text_Python
from backend.TextToSpeech import speak

tts_queue = asyncio.Queue()

async def tts_worker():
    while True:
        message = await tts_queue.get()
        try:
            await speak(message)
        except Exception as e:
            print("TTS Error:", e)
        tts_queue.task_done()


# Telegram Automation (GUI-based)
async def telegram_message(name, message):
    """Send a message to a contact by name using GUI automation"""
    try:
        open_app("telegram")
        time.sleep(5)

        # Search for contact
        time.sleep(1)
        pyautogui.hotkey("ctrl", "f")
        time.sleep(1)

        pyautogui.write(name, interval=0.05)
        time.sleep(1)

        pyautogui.press("enter")
        time.sleep(1)

        # Type and send message
        pyautogui.write(message, interval=0.05)
        time.sleep(1)

        pyautogui.press("enter")

        await tts_queue.put(f"Message sent to {name}")

    except Exception as e:
        print("Send Error:", e)
        await tts_queue.put("Sorry, I couldn't send the message.")


# Command Handler
async def handle_command(text):
    """Parse and handle send message commands"""
    text = text.lower().strip()

    if not text:
        return

    # Remove all platform indicators completely
    text = text.replace("in telegram", "").replace("on telegram", "").replace("via telegram", "").strip()
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

            await telegram_message(name, message)

        except Exception as e:
            print("ERROR:", e)
            await tts_queue.put("I couldn't understand. Who should I message on Telegram?")
            
            # Wait for TTS to finish before listening
            await asyncio.sleep(2)
            name = await asyncio.to_thread(Speech_To_Text_Python)

            await tts_queue.put("What should I say?")
            
            # Wait for TTS to finish before listening
            await asyncio.sleep(2)
            message = await asyncio.to_thread(Speech_To_Text_Python)

            if name and message:
                await telegram_message(name, message)


# Main Loop
async def main():
    asyncio.create_task(tts_worker())
    
    print("🤖 Telegram messenger running...")
    
    while True:
        print("Listening...")
        text = await asyncio.to_thread(Speech_To_Text_Python)

        if not text:
            continue

        print("You said:", text)
        await handle_command(text)


if __name__ == "__main__":
    asyncio.run(main())
