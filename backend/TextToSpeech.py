import asyncio
import edge_tts
import pygame
import os
import uuid

pygame.mixer.init()                     # ✅ FIX 1: Initialize mixer ONCE (moved outside function)

async def speak(text):
    filename = f"temp_response_{uuid.uuid4().hex}.mp3"

    communicate = edge_tts.Communicate(text, voice="en-US-ChristopherNeural")
    await communicate.save(filename)

    await asyncio.sleep(0.2)            # ✅ FIX 2: Wait for file write to complete

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()


    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)        # ✅ FIX 3: Non-blocking wait (replaced time.sleep)

    pygame.mixer.music.stop()
    pygame.mixer.music.unload()

    await asyncio.sleep(0.5)            # ✅ FIX 4: Allow Windows to release file before deletion

    try:
        if os.path.exists(filename):
            os.remove(filename)
    except Exception as e:
        print(f"Cleanup error: {e}")










