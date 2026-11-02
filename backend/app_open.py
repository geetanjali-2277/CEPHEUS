import pyautogui as gui
import time

def open_app(text):
    try:
        gui.press("win")
        time.sleep(0.2)
        gui.write(text)
        time.sleep(0.2)
        gui.press("enter")
    except Exception as e:
        pass






        
  

