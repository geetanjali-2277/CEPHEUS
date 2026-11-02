import asyncio
import os
from telethon import TelegramClient, events
from telethon.tl.types import User
from backend.speechtotext import Speech_To_Text_Python
from backend.TextToSpeech import speak 

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
phone_number = os.getenv("PHONE_NUMBER")


client = TelegramClient("jarvis_session", api_id, api_hash)

tts_queue = asyncio.Queue()

async def tts_worker():
    while True:
        message = await tts_queue.get()
        try:
            await speak(message)
        except Exception as e:
            print("TTS Error:", e)
        tts_queue.task_done()


# SEND FUNCTION 
async def telegram_send(chat_id, message):
    try:
        await client.send_message(chat_id, message)
        await tts_queue.put("Message sent successfully.")
    except Exception as e:
        print("Send Error:", e)
        await tts_queue.put("Sorry, I could not send the message.")


# REPLY FLOW
async def telegram_reply_flow(chat_id):
    await tts_queue.put("Do you want to reply?")

    # FIX: Wrap blocking call with asyncio.to_thread()
    answer = await asyncio.to_thread(Speech_To_Text_Python)
    answer = answer.lower()

    if "yes" in answer:
        await tts_queue.put("What is the message?")
        
        # FIX: Wrap blocking call with asyncio.to_thread()
        reply_text = await asyncio.to_thread(Speech_To_Text_Python)

        if reply_text:
            await telegram_send(chat_id, reply_text)
    else:
        await tts_queue.put("Okay, not replying.")



# Telegram message handler
@client.on(events.NewMessage)
async def handle_new_message(event):

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
    client.last_chat_id = event.chat_id

    # Start reply flow after speaking
    await telegram_reply_flow(event.chat_id)



# Main
async def main():
    await client.start(phone=phone_number)
    print("🤖 Jarvis Telegram listener running...")

    asyncio.create_task(tts_worker())

    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
