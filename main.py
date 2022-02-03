import os
import time

import client
import dotenv


env = dotenv.load_dotenv() #load env
discord = client.Gateway() #init discord gateway

discord.connect() #connect to ws://gateway.discord.gg
discord.identify(os.environ.get("DISCORD_TOKEN")) #identify token
discord.heartbeat(discord.heartbeat_interval) #start heartbeat loop

#listen events from websocket
@discord.listener("MESSAGE_CREATE") 
def new_message(event):
    name = event["d"]["author"]["username"] + "#" + event["d"]["author"]["discriminator"]
    message = event["d"]["content"]

    if message != "":
        print(f"{name} - {message}")

@discord.listener("READY") 
def ready(event):
    print("gateway ready!")


discord.listen() #start event listen loop


while True: #MainThread 
    time.sleep(1)