import asyncio
import os
from backend.automation_brain import brain
from backend.speechtotext import Speech_To_Text_Python
from telethon import TelegramClient, events
from telethon.tl.types import User
from backend.TextToSpeech import speak

# Telegram configuration
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
phone_number = os.getenv("PHONE_NUMBER")

# Create Telegram client
telegram_client = TelegramClient("jarvis_session", api_id, api_hash)
tts_queue = asyncio.Queue()

# Flag to prevent voice listening while TTS is active
tts_active = asyncio.Event()
tts_active.set()  # Start as "not speaking"

# Flag to prevent voice listening while Telegram reply is in progress
telegram_reply_in_progress = asyncio.Event()
telegram_reply_in_progress.set()  # Start as "not in reply mode"


async def tts_worker():
    """Handle text-to-speech announcements from queue"""
    while True:
        message = await tts_queue.get()
        try:
            # Signal that TTS is active
            tts_active.clear()
            await speak(message)
        except Exception as e:
            print("TTS Error:", e)
        finally:
            # Give audio extra time to finish playing before setting flag
            await asyncio.sleep(1)
            # Signal that TTS is done
            tts_active.set()
            await asyncio.sleep(0.5)  # Small delay before next message
        tts_queue.task_done()


async def telegram_reply_flow(chat_id):
    """Handle reply flow for Telegram messages"""
    # Signal that Telegram reply is in progress
    telegram_reply_in_progress.clear()
    
    try:
        # Add delay to let voice loop detect the flag change
        await asyncio.sleep(2)
        
        await tts_queue.put("Do you want to reply?")
        
        # Wait for TTS to finish before listening
        await tts_active.wait()
        await asyncio.sleep(4)
        
        # Get voice response
        answer = await asyncio.to_thread(Speech_To_Text_Python)
        answer = answer.lower().strip()
        
        print(f"DEBUG -> Reply response: '{answer}'")
        
        # Better yes/no detection
        if any(word in answer for word in ["yes", "yeah", "yep", "sure", "okay", "ok"]):
            await tts_queue.put("What is the message?")
            
            # Wait for TTS to finish before listening
            await tts_active.wait()
            await asyncio.sleep(4)
            
            reply_text = await asyncio.to_thread(Speech_To_Text_Python)
            reply_text = reply_text.strip()
            
            print(f"DEBUG -> Message: '{reply_text}'")

            if reply_text:
                try:
                    await telegram_client.send_message(chat_id, reply_text)
                    await tts_queue.put("Message sent successfully.")
                except Exception as e:
                    print("Send Error:", e)
                    await tts_queue.put("Sorry, I could not send the message.")
            else:
                await tts_queue.put("Sorry, I didn't catch that. Message not sent.")
        else:
            await tts_queue.put("Okay, not replying.")
    finally:
        # Signal that Telegram reply is done
        telegram_reply_in_progress.set()


@telegram_client.on(events.NewMessage)
async def handle_new_message(event):
    """Handle incoming Telegram messages"""
    sender = await event.get_sender()
    chat = await event.get_chat()

    sender_name = (
        sender.first_name if isinstance(sender, User) and sender.first_name else
        chat.title if hasattr(chat, "title") else
        "Someone"
    )

    message = event.message.message
    if not message:
        return

    sentence = f"New Telegram message from {sender_name}. {message}"
    print(sentence)

    await tts_queue.put(sentence)
    
    # Save last chat
    telegram_client.last_chat_id = event.chat_id

    # Start reply flow after speaking
    await telegram_reply_flow(event.chat_id)


async def voice_command_loop():
    """Main voice command recognition loop"""
    print("🎤 Voice command listener started...")
    await asyncio.sleep(1)  # Initial delay
    
    while True:
        try:
            # Skip listening if Telegram reply is in progress
            if not telegram_reply_in_progress.is_set():
                await asyncio.sleep(1)
                continue
            
            # Wait for TTS to finish before listening
            await tts_active.wait()
            
            # Add longer delay to ensure audio has completely finished
            await asyncio.sleep(2)
            
            # Run blocking speech recognition in thread to prevent blocking async loop
            recognized_text = await asyncio.to_thread(Speech_To_Text_Python)
            
            if not recognized_text:
                continue
                
            if "stop" in recognized_text.lower():
                print("🛑 Stop command received. Exiting.")
                break
                
            await brain(recognized_text)
        except Exception as e:
            print(f"Voice command error: {e}")


async def main():
    """Main async function - runs Telegram and voice commands simultaneously"""
    print("🤖 Jarvis starting with Telegram integration...")
    
    try:
        # Connect Telegram client
        await telegram_client.start(phone=phone_number)
        print("✅ Telegram connected and listening...")
        
        # Start TTS worker
        asyncio.create_task(tts_worker())
        
        # Run voice command loop and Telegram listener simultaneously
        await asyncio.gather(
            voice_command_loop(),
            telegram_client.run_until_disconnected()
        )
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await telegram_client.disconnect()
        print("🛑 Jarvis stopped.")


if __name__ == "__main__":
    asyncio.run(main())

