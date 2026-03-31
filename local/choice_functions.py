import json
import keyboard
import mouse
import statistics
import time
import sys
import requests
import random
import psutil
import threading

#works
def load_config():
    with open("etc/config.json", "r") as config:
        settings = json.load(config)
        config.close
        return(settings)

def find_game():
    settings = load_config()
    for p in psutil.process_iter(["name"]):
        if settings["game"].lower() in p.info["name"].lower():
            return(p)
    return(None)

_slowmo_running = False
_slowmo_thread = None
_force_pause_slowmo = False
def _slowmo_loop():
    proc = find_game()
    if not proc:
        print("Game not found")
        return()
    while _slowmo_running:
        try:
            if _force_pause_slowmo:
                proc.resume()
                time.sleep(0.01)
                continue
            proc.suspend()
            time.sleep(1-settings_cache["slow"]*settings_cache["smooth"])
            proc.resume()
            time.sleep(settings_cache["slow"]*settings_cache["smooth"])
        except (psutil.NoSuchProcess):
            print("Game doesnt exist")
            break
        except (psutil.AccessDenied):
            print("Access denied")
            break
        try:
            proc.resume()
        except:
            pass

settings_cache = {}
def start_slowmo():
    global _slowmo_running, _slowmo_thread
    settings_cache.update(load_config())
    _slowmo_running = True
    _slowmo_thread = threading.Thread(target = _slowmo_loop, daemon = True)
    _slowmo_thread.start()

def stop_slowmo():
    global _slowmo_running
    _slowmo_running = False
    if _slowmo_thread:
        _slowmo_thread.join(timeout = 3)


def load_list_of_votes():
    with open("etc/votes.json", "r") as config:
        votes = json.load(config)
        config.close
        return(votes)

def kill():
    print("Do you want to end? (y/n)")
    if input() == "y":
        sys.exit()

def update():
    settings = load_config()
    try:
        requests.get(f"{settings["hostport"]}/update")
    except:
        time.sleep(0.5)
        return("server is not open")
    return("updated")

def awaken():
    settings = load_config()
    try:
        requests.get(f"http://{settings["hostport"]}/awake")
    except:
        return(False)
    return(True)

def collect_votes():
    settings = load_config()
    for x in range (0, settings["wait"]*10):
        results = load_list_of_votes()
        if results["flag"] == True:
            break
        time.sleep(0.1)
        if x % 10 == 0:
            timeleft = settings["wait"] - x/10
            print(str(timeleft))
    return(results["votes"])

def sensible_choice(list_of_votes):
    chosen = statistics.mode(list_of_votes)
    return(chosen)

def chaos_choice(list_of_votes):
        chosenid = random.randint(0,len(list_of_votes)-1)
        chosen=list_of_votes[chosenid]
        return(chosen)

def unpause():
    settings = load_config()
    if settings["pause"] != 0:
        keyboard.send(settings["listen"])
        time.sleep(settings["pause"])
        return()
    return()

def click_on_choice(chosen):
    return_position = mouse.get_position()
    mouse.move(chosen[0],chosen[1], absolute=True)
    mouse.click(button="left")
    mouse.move(return_position[0],return_position[1], absolute=True)

def press_choice_button(chosen):
    keyboard.send(f"{chosen}")

def summerize_votes():
    results = load_list_of_votes()
    votes = results["votes"]
    settings = load_config()
    summary = "\n \n"
    for x in range(0, len(settings["buttons"])):
        button_votes = votes.count(settings["buttons"][x])
        summary = f"""{summary}{settings["choice_names"][x]} had {button_votes} votes \n"""
    return(summary)

def make_choice_and_send_it():
    global _force_pause_slowmo
    settings = load_config()
    if not awaken():
        print("server is not open")
        return()
    print("awoken")
    if settings["slowmo"]:
        start_slowmo()
    list_of_votes = collect_votes()
    if settings["chaos"]:
        chosen = chaos_choice(list_of_votes)
    else:
        chosen = sensible_choice(list_of_votes)
    print(summerize_votes())
    if settings["slowmo"]:
        _force_pause_slowmo = True
        time.sleep(0.05)
    
    if settings["use_mouse"]:
        click_on_choice(chosen)
    else:
        press_choice_button(chosen)
    if settings["slowmo"]:
        _force_pause_slowmo = False
        stop_slowmo()
    winnermessage = choose_message(chosen)
    print(winnermessage)


def choose_message(chosen):
    settings = load_config()
    with open("etc/winner_messages.json") as message:
        allMessages = json.load(message)
        message.close()
    button = settings["buttons"].index(chosen)
    choice = random.randint(0, len(allMessages["messages"])-1)
    choice_message = allMessages["messages"][choice]
    winnermessage = f"{choice_message[0]}{settings["choice_names"][button]}{choice_message[1]}"
    return(winnermessage)