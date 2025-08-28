"""
Listenbutton                    :   listen
Update                          :   update
Kill                            :   kill

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
import sys
import mouse as gestapo
import json

while True:
    print("Skip setup? (y/n)")
    if input() == "y":
        sys.exit()
    print("Button to start choice")
    listen = str(input())
    print("Is this the pause button? (y/n)")
    if input() == "y":
        print("How long between unpause to choice press?")
        pause = int(input())
    else:
        pause = 0
    print("Button to update server")
    update = str(input())
    print("Button to stop program")
    kill = str(input())

    print("How long time to vote in seconds")
    wait = int(input())

    print("How many players?")
    players = int(input())
    print("How many degrees of freedom? (random votes)")
    dof = int(input())
    print("How many choices?")
    choices = int(input())
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
    hostport = input()
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
        with open("etc/config.json", "w") as out:
            json.dump(config, out)
        sys.exit()