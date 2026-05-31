""" Using Google TTS to speak CZ text highlited by mouse """
from pynput import mouse
from gtts import gTTS
import os
import pyautogui
import time
import pyperclip
import queue
import sys

text_old = ''

def on_click(x,y,button, pressed, injected):
    global text_old
    if not injected and button == mouse.Button.left and pressed == False:
        time.sleep(0.01)
        # time.sleep(0.35)  # longer delay needed for work with old application like Notepad
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.01)
        _text = pyperclip.paste().strip()
        if _text and _text != text_old:
            tts_queue.put(_text)
            text_old = _text

tts_queue = queue.Queue()

listener = mouse.Listener(on_click=on_click)
listener.start()

try:
    while True:
        try:
            text = tts_queue.get(timeout=0.1)
            if text is None:
                break

            tts = gTTS(text=text, lang='cs')
            tts.save("out.mp3")
            os.system("start out.mp3")  # Windows
            # os.system("mpg123 out.mp3") # Linux

            tts_queue.task_done()
            time.sleep(0.01)
        except queue.Empty:
            continue

except KeyboardInterrupt:
    print('\n[INFO] Keyboard interrupt detected.')
except Exception as e_msg:
    print(f'\n[INFO] Exception with error message: {e_msg}')
finally:
    print(f'Interrupt registered. Terminating the program...')
    if listener.running:
        listener.stop()
    tts_queue.put(None)
    sys.exit(0)
