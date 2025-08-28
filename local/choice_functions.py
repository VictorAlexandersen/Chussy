import json
import keyboard
import mouse
import statistics
import time
import sys
import requests
import random

#works
def load_config():
    with open("etc/config.json", "r") as config:
        settings = json.load(config)
        config.close
        return(settings)

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
    settings = load_config()
    if not awaken():
        print("server is not open")
        return()
    print("awoken")
    list_of_votes = collect_votes()
    if settings["chaos"]:
        chosen = chaos_choice(list_of_votes)
    else:
        chosen = sensible_choice(list_of_votes)
    print(summerize_votes())
    if settings["use_mouse"]:
        click_on_choice(chosen)
    else:
        press_choice_button(chosen)
    print(f"Winner winner, chicken dinner, Mr {chosen}")
    
