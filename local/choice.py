import keyboard
import choice_functions as cf

settings = cf.load_config()
while True:
    key = keyboard.read_key()
    if key == settings["listen"]:
        cf.make_choice_and_send_it()
    if key == settings["kill"]:
        cf.kill()
    if key == settings["update"]:
        cf.update()
        settings = cf.load_config()


"""while True:
    key = keyboard.read_key()
    if key==listenbutton:
        votingprocess()
    if key == updatebutton:
        update_settings()
    if key == exitbutton:
        exit()"""