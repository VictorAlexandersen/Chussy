import keyboard
import choice_functions as cf
import time
import sys

settings = cf.load_config()
try:
    while True:
        key = keyboard.read_key()
        if key == settings["listen"]:
            cf.crash()
            cf.make_choice_and_send_it()
        if key == settings["kill"]:
            cf.kill()
        if key == settings["update"]:
            cf.update()
            settings = cf.load_config()
except Exception as e:
    crash=["Error on line {}".format(sys.exc_info()[-1].tb_lineno),"\n",e]
    print(crash)
    timeX=str(time.time())
    with open("crashlogs/CRASH-"+timeX+".txt","w") as crashLog:
        crashLog.write("\n".join(map(str, crash)))


"""while True:
    key = keyboard.read_key()
    if key==listenbutton:
        votingprocess()
    if key == updatebutton:
        update_settings()
    if key == exitbutton:
        exit()"""