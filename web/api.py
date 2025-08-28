from flask import Flask, request
import json
import time
import random
import api_functions as api
api.write_html()
app = Flask(__name__)


@app.route("/", methods=["GET"])
def land():
    return(api.land())

@app.route("/vote", methods=["GET"])
def vote():
    return(api.count_vote())

@app.route("/awake", methods=["GET"])
def awake():
    api.awake()
    return("")

@app.route("/update")
def update():
    api.write_html
    return("")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)