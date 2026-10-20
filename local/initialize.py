"""
Listenbutton                    :   listen
Update                          :   update
Kill                            :   kill
Slowmo                          :   slowmo
    Game                        :   game
    Slow amount                 :   slow
    Smoothness of slow game     :   smooth

Wait                            :   wait
Pause                           :   pause

Players                         :   players
Degrees of freedom              :   dof


Amount of choices               :   choices
Keyboard or mouse for presses   :   use_mouse
Buttons                         :   buttons
Mouse positions                 :   positions
    Choice names                :   choice_name

Chaos modus                     :   chaos

Hostport                        :   hostport

"""
import os
import sys
import mouse as gestapo
import json

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "etc", "config.json")

while True:
    if input("Skip setup? (y/n) ") == "y":
        sys.exit()
    # defaults, so the config can still be written if slowmo is skipped
    game, slowmo, slow, smooth = "", False, 0.5, 1.0
    listen = str(input("Button to start choice "))
    if input("Is this the pause button? (y/n) ") == "y":
        print("How long between unpause to choice press? ")
        pause = float(input())
    else:
        pause = 0
    update = str(input("Button to update server "))
    kill = str(input("Button to stop program "))
    if pause == 0:
        if input("Slowmotion on? (y/n) ") == "y":
            game = str(input("Game name lol "))
            slowmo = True
            slow = float(input("How much slower (0,1) where low is slow "))
            smooth = float(input("How smooth (0,1), 0 is smooth but takes more computing "))
    wait = int(input("How long time to vote in seconds "))

    players = int(input("How many players? "))
    dof = int(input("How many degrees of freedom? (random votes) "))
    choices = int(input("How many choices?" ))
    choice_name = []
    buttons = []

    print("Use the mouse to press the choices?(y/n)")
    if input() == "y":
        use_mouse = True
        for x in range(0,choices):
            print(f"Click where choice {x+1} is gonna be")
            gestapo.wait(button="left")
            position = gestapo.get_position()
            buttons.append(position)
            print("Name of this button")
            button_name = input()
            choice_name.append(button_name)
            
    else:
        use_mouse = False
        for x in range(0, choices):
            print(f"What button to press for choice {x+1}")
            button = input()
            buttons.append(button)
            print("Name of this button")
            button_name = input()
            choice_name.append(button_name)
    print("Whats the hostport?")
    hostport = input().strip().rstrip("/")
    print("Chaos-Modus active?(y/n)")
    if input() == "y":
        chaos = True
    else:
        chaos = False
    config = {
        "listen"        : listen,
        "update"        : update,
        "kill"          : kill,
        "wait"          : wait,
        "pause"         : pause,
        "game"          : game,
        "slowmo"        : slowmo,
        "slow"          : slow,
        "smooth"        : smooth,
        "players"       : players,
        "dof"           : dof,
        "choices"       : choices,
        "use_mouse"     : use_mouse,
        "buttons"       : buttons,
        "choice_names"  : choice_name,
        "chaos"         : chaos,
        "hostport"      : hostport
    }
    print("this u? (y/n)")
    print(config)
    if input() == "y":
        with open(CONFIG_PATH, "w") as out:
            json.dump(config, out)
        sys.exit()