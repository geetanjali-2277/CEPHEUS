import speech_recognition as sr

def Speech_To_Text_Python():
    r = sr.Recognizer()
    r.pause_threshold = 1.5  # Increased from 0.5 to allow more time for user to speak
    r.energy_threshold = 150  # Slightly lowered to capture quieter speech
    mic = sr.Microphone()

    print("🎤 Listening... Go ahead and speak!")

    try:
        with mic as source:
            # Added timeout to wait up to 10 seconds for speech
            audio = r.listen(source, timeout=10, phrase_time_limit=10)

        text = r.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print("API error:", e)
        return ""
    except sr.RequestError:
        return ""
