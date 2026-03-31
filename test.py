import psutil
import keyboard  # pip install keyboard
import time
import threading

GAME_NAME = "Game.exe"
slow_factor = 0.3
running = False

def find_proc():
    for p in psutil.process_iter(['name']):
        if GAME_NAME.lower() in p.info['name'].lower():
            return p
    return None

def slow_loop():
    proc = find_proc()
    if not proc:
        print("Game not found!")
        return
    while running:
        proc.suspend()
        time.sleep(1 - slow_factor)
        proc.resume()
        time.sleep(slow_factor)
    proc.resume()  # make sure it's resumed when toggled off

thread = None

def toggle(e):
    global running, thread
    running = not running
    if running:
        print("Slow-mo ON")
        thread = threading.Thread(target=slow_loop, daemon=True)
        thread.start()
    else:
        print("Slow-mo OFF")

keyboard.on_press_key("F8", toggle)
print("Press F8 to toggle slow-mo. Ctrl+C to quit.")
keyboard.wait()