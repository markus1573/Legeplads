import time
import sys
import threading
import pyautogui as ag
from pynput.keyboard import Listener, KeyCode, Key, HotKey

delay = 0.008 if sys.platform == "darwin" else 0.025
start_stop_key = KeyCode.from_char("s")
combination = {KeyCode.from_char('q')}
# combination = {Key.cmd,KeyCode.from_char('b')}


class ClickMouse(threading.Thread):
    def __init__(self,loc):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.running = False
        self.program_running = True
        self.loc = loc

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False
    
    def run(self):
        while self.program_running:
            while self.running:
                    ag.click(self.loc,_pause=False)
                    time.sleep(self.delay)
            time.sleep(0.1)

def Run_autoclicker(loc=None):
    click_thread = ClickMouse(loc)
    click_thread.start()
    current = set()

    def Toggle(key):
        if key == start_stop_key:
            if click_thread.running:
                click_thread.stop_clicking()
            else:
                click_thread.start_clicking()
        elif key in combination:
            current.add(key)
            if all(k in current for k in combination):
                click_thread.exit()
                listener.stop()
        elif key == hotkey:
            click_thread.exit()
            listener.stop()
    
    def for_canonical(f):
        return lambda k: f(listener.canonical(k))
    
    def exit_autoclicker():
        click_thread.exit()
        listener.stop()
    
    hotkey = HotKey(HotKey.parse('<shift>+q'), on_activate=exit_autoclicker)

    with Listener(on_press=Toggle) as listener:
        listener.join()

def start_autoclicker_standalone(loc=None,daemon:bool=False):
    autoclicker_thread = threading.Thread(target=Run_autoclicker, args=[loc], daemon=daemon)
    autoclicker_thread.start()




if __name__ == '__main__':
    start_autoclicker_standalone((1000,500))