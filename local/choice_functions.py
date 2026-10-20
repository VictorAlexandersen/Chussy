import json
import os
import random
import threading
import time
from collections import Counter

import keyboard
import mouse
import psutil
import requests

# etc/ and crashlogs/ sit next to local/, so this works no matter which
# folder you start the script from.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "etc", "config.json")
VOTES_PATH = os.path.join(BASE_DIR, "etc", "votes.json")
MESSAGES_PATH = os.path.join(BASE_DIR, "etc", "winner_messages.json")

HTTP_TIMEOUT = 3  # seconds; without this requests can hang forever


def load_config():
    with open(CONFIG_PATH, "r") as config:
        return json.load(config)


def find_game():
    name = load_config()["game"].lower()
    for p in psutil.process_iter(["name"]):
        # info["name"] is None for processes we're not allowed to inspect
        if name in (p.info["name"] or "").lower():
            return p
    return None


# --------------------------------------------------------------------------
# Slow motion: rapidly suspend/resume the game process.
#   slow   = fraction of time the game is running (0-1)
#   smooth = length of one suspend/resume cycle in seconds (small = smoother)
# --------------------------------------------------------------------------
_stop_event = threading.Event()
_slowmo_thread = None


def _slowmo_loop(proc, slow, period):
    run_time = slow * period
    freeze_time = (1 - slow) * period
    try:
        while not _stop_event.is_set():
            proc.suspend()
            # Event.wait() returns True immediately if stop is requested, so we
            # never sit frozen for up to a second after stop_slowmo() is called.
            if _stop_event.wait(freeze_time):
                break
            proc.resume()
            if _stop_event.wait(run_time):
                break
    except psutil.NoSuchProcess:
        print("Game doesnt exist")
    except psutil.AccessDenied:
        print("Access denied (try running as administrator)")
    finally:
        # Whatever happened, never leave the game frozen.
        try:
            proc.resume()
        except Exception:
            pass


def start_slowmo():
    """Returns True if slowmo actually started."""
    global _slowmo_thread
    settings = load_config()
    proc = find_game()
    if proc is None:
        print("Game not found")
        return False
    slow = min(max(float(settings["slow"]), 0.01), 1.0)
    period = max(float(settings["smooth"]), 0.03)  # timers can't do much below ~15ms
    _stop_event.clear()
    _slowmo_thread = threading.Thread(
        target=_slowmo_loop, args=(proc, slow, period), daemon=True
    )
    _slowmo_thread.start()
    return True


def stop_slowmo():
    """Stops slowmo and returns once the game has been resumed."""
    _stop_event.set()
    if _slowmo_thread:
        _slowmo_thread.join(timeout=3)


# --------------------------------------------------------------------------
# Votes / server
# --------------------------------------------------------------------------
def load_list_of_votes():
    # The server may be mid-write, which gives a half-written (invalid) file.
    for _ in range(5):
        try:
            with open(VOTES_PATH, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            time.sleep(0.05)
    return {"votes": [], "flag": False}


def kill():
    print("Do you want to end? (y/n)")
    if input() == "y":
        raise SystemExit


def _server_url(path):
    host = load_config()["hostport"].strip().rstrip("/")
    if not host.startswith(("http://", "https://")):
        host = "http://" + host
    return f"{host}/{path}"


def update():
    try:
        requests.get(_server_url("update"), timeout=HTTP_TIMEOUT)
    except requests.RequestException:
        time.sleep(0.5)
        return "server is not open"
    return "updated"


def awaken():
    try:
        requests.get(_server_url("awake"), timeout=HTTP_TIMEOUT)
    except requests.RequestException:
        return False
    return True


def collect_votes():
    settings = load_config()
    results = {"votes": [], "flag": False}
    for x in range(int(settings["wait"] * 10)):
        results = load_list_of_votes()
        if results["flag"]:
            break
        if x % 10 == 0:
            print(settings["wait"] - x // 10)
        time.sleep(0.1)
    return results["votes"]


def sensible_choice(list_of_votes):
    # Counter on JSON strings so it also works when a vote is a [x, y] list
    # (lists are unhashable, which broke statistics.mode in mouse mode).
    counts = Counter(json.dumps(v) for v in list_of_votes)
    return json.loads(counts.most_common(1)[0][0])


def chaos_choice(list_of_votes):
    return random.choice(list_of_votes)


def unpause():
    settings = load_config()
    if settings["pause"] != 0:
        keyboard.send(settings["listen"])
        time.sleep(settings["pause"])


def click_on_choice(chosen):
    return_position = mouse.get_position()
    mouse.move(chosen[0], chosen[1], absolute=True)
    time.sleep(0.05)   # let the game see the cursor arrive
    mouse.click(button="left")
    time.sleep(0.05)   # don't move the cursor away mid-click
    mouse.move(return_position[0], return_position[1], absolute=True)


def press_choice_button(chosen):
    # keyboard.send() presses and releases instantly, which games that poll
    # input once per frame can miss. Hold it briefly instead.
    keyboard.press(f"{chosen}")
    time.sleep(0.05)
    keyboard.release(f"{chosen}")


def summerize_votes(votes, settings):
    summary = "\n \n"
    for button, name in zip(settings["buttons"], settings["choice_names"]):
        summary += f"{name} had {votes.count(button)} votes \n"
    return summary


def choose_message(chosen, settings):
    with open(MESSAGES_PATH, "r") as message:
        all_messages = json.load(message)
    try:
        name = settings["choice_names"][settings["buttons"].index(chosen)]
    except ValueError:
        name = str(chosen)
    before, after = random.choice(all_messages["messages"])
    return f"{before}{name}{after}"


def make_choice_and_send_it():
    settings = load_config()
    if not awaken():
        print("server is not open")
        return
    print("awoken")

    slowmo_on = settings["slowmo"] and start_slowmo()
    try:
        votes = collect_votes()
    finally:
        # runs even if collecting crashes, so the game can't stay frozen
        if slowmo_on:
            stop_slowmo()

    if not votes:
        print("Nobody voted - picking a random button")
        chosen = random.choice(settings["buttons"])
    elif settings["chaos"]:
        chosen = chaos_choice(votes)
    else:
        chosen = sensible_choice(votes)
    print(summerize_votes(votes, settings))

    time.sleep(0.05)  # let the game wake up before we press anything
    unpause()  # only does something if "pause" != 0 in the config
    if settings["use_mouse"]:
        click_on_choice(chosen)
    else:
        press_choice_button(chosen)

    print(choose_message(chosen, settings))
