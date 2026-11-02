
from .app_open import open_app
import time
import pyautogui

def play_music_on_spotify(query):
    open_app("spotify")
    time.sleep(8)
    pyautogui.click(500, 300) 
    time.sleep(1)
    pyautogui.hotkey("ctrl", "k")
    time.sleep(1)
    pyautogui.write(query, interval=0.05)     
    pyautogui.press("enter")
    time.sleep(4)
    pyautogui.press("enter")



