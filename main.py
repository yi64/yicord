import os
import sys
import time

import client
import dotenv


env = dotenv.load_dotenv() #load env
token = os.environ.get("DISCORD_TOKEN")

gateway = client.Gateway() #init discord gateway
user = client.User() #init discord http api

gateway.connect() #connect to ws://gateway.discord.gg
gateway.identify(token) #identify token
gateway.heartbeat(gateway.heartbeat_interval) #start heartbeat loop

user.identify(token) #identify user token

 
#listen events from websocket
@gateway.listener("MESSAGE_CREATE") 
def new_message(event):
    name = event["d"]["author"]["username"] + "#" + event["d"]["author"]["discriminator"]
    message = event["d"]["content"]

    if message != "":
        print(f"{name} - {message}")

@gateway.listener("READY") 
def ready(event):
    print("gateway ready!")


gateway.listen() #start event listen loop


while True: #MainThread 
    time.sleep(1)