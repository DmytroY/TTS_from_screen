from pynput import keyboard
import pyttsx3
import threading
import queue

active_listener_flag = True
tts_queue = queue.Queue()

def tts_worker():
    while True:
        text_to_say = tts_queue.get()
        if text_to_say == None:
            break
        # unfortunately pyttsx3 should be reinitialized to work in thread.
        tts_engine = pyttsx3.init()
        tts_engine.say(text_to_say)
        tts_engine.runAndWait()
        print(f'saying: {text_to_say}')
        tts_queue.task_done()

tts_thread = threading.Thread(target=tts_worker, daemon=True)
tts_thread.start()

def on_press(key):
    global active_listener_flag
    tts_queue.put(str(key).strip("'"))
    
def on_release(key):
    global active_listener_flag
    if key == keyboard.Key.esc:
        active_listener_flag = False
        tts_queue.put(None)
        return False

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

while active_listener_flag:
    pass