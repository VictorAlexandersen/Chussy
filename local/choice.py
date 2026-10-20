import os
import time
import traceback

import keyboard
import choice_functions as cf


def log_crash():
    crash_dir = os.path.join(cf.BASE_DIR, "crashlogs")
    os.makedirs(crash_dir, exist_ok=True)  # otherwise the crash log itself crashes
    path = os.path.join(crash_dir, f"CRASH-{time.time()}.txt")
    with open(path, "w") as crash_log:
        crash_log.write(traceback.format_exc())  # full traceback, real line numbers
    return path


settings = cf.load_config()
while True:
    try:
        # read_key() fires on key DOWN and key UP, so every press used to
        # trigger twice. Only react to key-down events.
        event = keyboard.read_event()
        if event.event_type != keyboard.KEY_DOWN:
            continue
        key = event.name

        if key == settings["listen"]:
            cf.make_choice_and_send_it()
        elif key == settings["kill"]:
            cf.kill()
        elif key == settings["update"]:
            print(cf.update())
            settings = cf.load_config()
    except Exception:
        # Log it and keep listening instead of ending the whole program.
        print("Crashed, log saved to", log_crash())
        traceback.print_exc()
        time.sleep(1)  # avoid a tight crash loop
