import pyttsx3
from pynput import keyboard
import queue

c_list = []
flag = True
stopword = 'stopit'
tts_queue = queue.Queue()
tts_engine = pyttsx3.init()

print(f'This will say every word you print. For exit print: {stopword}')

def on_press(key):
    global c_list, flag, stopword
    c = str(key).strip("'")

    if c == 'Key.backspace':
        if c_list:
            c_list.pop()

    if len(c) == 1:
        c_list.append(c)

    if c in ('Key.space', 'Key.enter', '.', ',', '!', ':', ';', '?'):
        word = ''.join(c_list)
        if word == stopword:
            tts_queue.put(None)
            flag = False
            return None
        tts_queue.put(word)
        print(word)
        c_list.clear()

listener = keyboard.Listener(on_press=on_press)
listener.start()

while flag:
    try:
        word = tts_queue.get()
        if word:
            tts_engine.say(word)
            tts_engine.runAndWait()
        tts_queue.task_done()
    except queue.Empty:
        continue

if listener.running:
        listener.stop()