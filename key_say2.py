from pynput import keyboard
import pyttsx3
import queue

active_listener_flag = True

tts_engine = pyttsx3.init()
tts_queue = queue.Queue()

def on_press(key):
    # print(f'Pressed {key}')
    tts_queue.put(str(key).strip("'"))
    
def on_release(key):
    # print(f'released {key}')
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
    try:
        text = tts_queue.get()
        if text is None:
            break
        tts_engine.say(text)
        tts_engine.runAndWait()
        print(f'Saying: {text}')
        tts_queue.task_done()
    except queue.Empty:
        continue