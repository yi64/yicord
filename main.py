from concurrent.futures import thread
import json
import os
import sys
import threading
import time
import webbrowser
import webview

import client
import dotenv
import flask

from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

env = dotenv.load_dotenv() #load env
token = os.environ.get("DISCORD_TOKEN")


app = flask.Flask(__name__)
socketio = SocketIO(app)

gateway = client.Gateway() #init discord gateway
user = client.User() #init discord http api

gateway.connect() #connect to ws://gateway.discord.gg
gateway.identify(token) #identify token
gateway.heartbeat(gateway.heartbeat_interval) #start heartbeat loop
_ready = False #gateway ready status

user.identify(token) #identify user token

dms = []
 
#listen events from websocket
index = [0]
@gateway.listener("MESSAGE_CREATE") 
def new_message(event):
    name = event["d"]["author"]["username"] + "#" + event["d"]["author"]["discriminator"]
    message = event["d"]["content"]

    if name == "yki#8153":
        json.dump(event, open(f"{index[0]}.json", "w"))

        index[0] += 1


@gateway.listener("READY") 
def ready(event):
    global _ready

    dms = user.fetch_dms(event)

    socketio.emit("ready", dms, broadcast=True)

    json.dump(event, open("ready.json", "w"))
    _ready = True

gateway.listen() #start event listen loop

@app.route("/")
def index():
    return flask.render_template("app.html")


if __name__ == "__main__":
    webview.create_window('YiCord', 'http://127.0.0.1:5544', width=1000, height=600, text_select=True)
    threading.Thread(target=socketio.run, args=(app, "127.0.0.1", 5544), daemon=True).start()

    webview.start()

    