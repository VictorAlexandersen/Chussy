import json
import random
import time
from flask import request
#works
def load_config():
    with open("etc/config.json", "r") as config:
        settings = json.load(config)
        config.close
        return(settings)
#changed
def write_html():
    settings = load_config()

    grid = []
    for x in range(0, len(settings["choice_names"])):
        grid.append(f"""<a href="http://{settings["hostport"]}/vote?vote={x}"><div class="box"> {settings["choice_names"][x]}</div></a>""")
    wrapper = ""
    for x in range(0,len(grid)):
        wrapper = f"""{wrapper}   {grid[x]}"""

    votetime_start = """<!DOCTYPE html>
    <html>
    <head>
    <style>
    body{
        height: 100%;
        background-color: grey;
    }

    .wrapper {
        display: grid;
        min-width: 100vw;
        min-height: 100vh;
        grid-template-columns: 1fr 1fr;
        column-gap: 5vw;
        row-gap: 5vh;
        border: 10px;
        border-color: black;
        }

    .box {
        display: flex;
        height: 100%;
        width: 100%;
        color: black;
        background-color: white;
        justify-content: center;
        align-items: center;
        font-size: 200%;
    }
    </style>
    <body> 
    <div class="wrapper">"""

    votetime_end = """</div>
    </body>"""

    straightback = f"""<!DOCTYPE html>
    <html>
        <head>
            <meta http-equiv="refresh", content="{0};url=http://{settings["hostport"]}/">
        </head>
    </html>"""

    confirmvote = f"""<!DOCTYPE html>
    <html>
        <head>
            <meta http-equiv="refresh", content="3;url=http://{settings["hostport"]}/"/>
        </head>
        <p>yipii :D</p>
    </html>"""
    votetime = f"{votetime_start} {wrapper} {votetime_end}"

    straightback_writer = open("web/straightback.html", "w")
    straightback_writer.write(straightback)
    straightback_writer.close()

    confirmvote_writer = open("web/confirmvote.html", "w")
    confirmvote_writer.write(confirmvote)
    confirmvote_writer.close()

    votetime_writer = open("web/votetime.html", "w")
    votetime_writer.write(votetime)
    votetime_writer.close()
#works
def awake():
    settings = load_config()
    votes = list()
    for x in range(0,settings["dof"]):
        crazy = random.randint(0,len(settings["buttons"])-1)
        votes.append(settings["buttons"][crazy])

    flag = False

    structure = {"votes": votes,
                 "flag": flag}
    with open("etc/votes.json", "w") as newvote:
        json.dump(structure, newvote)
        newvote.close
    awake = time.time()
    with open("etc/time.json", "w") as awaketime:
        json.dump(awake, awaketime)
        awaketime.close
    return("")
#works
def count_vote():
    settings = load_config()
    with open("etc/time.json", "r") as awake:
        start = json.load(awake)

    timepassed = time.time() - start
    if timepassed < settings["wait"]:
        with open("etc/votes.json", "r") as readvotes:
            current_votes = json.load(readvotes)
            readvotes.close

        if current_votes["flag"]:
            payload = open("web/straightback.html", "r")
            return(payload)
        
        vote_number = int(request.args.get("vote"))
        print(vote_number)
        vote = settings["buttons"][vote_number]
        current_votes["votes"].append(vote)

        if len(current_votes["votes"]) == settings["players"] + settings["dof"]:
            current_votes["flag"] = True

        with open("etc/votes.json", "w") as writevotes:
            json.dump(current_votes, writevotes)
            writevotes.close
        payload = open("web/confirmvote.html", "r")
        return(payload)
    else:
        payload = open("web/straightback.html", "r")
        return(payload)
#works
def land():
    payload = open("web/votetime.html", "r")
    return(payload)


