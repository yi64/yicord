import websocket

import time
import ujson
import random
import threading

from typing import List, Union


class Gateway():
    def __init__(self) -> None:
        self.seq: Union[None, str] = None
        self.open: bool = False
        self.debug: bool = False
        self.version: int = 9
        self.handlers: List[dict] = []
        self.heartbeat_interval: Union[None, int] = None
        self.uri: str = f"wss://gateway.discord.gg/?v={self.version}&encoding=json"

        self.ws: websocket.WebSocket = websocket.WebSocket()

    def recv_json(self) -> Union[dict, None]:
        try:
            return ujson.loads(self.ws.recv())
        except:
            return None

    def send_json(self, data: dict) -> None:
        self.ws.send(ujson.dumps(data))

    def heartbeat(self, delay, threaded=True) -> None:
        if threaded:
            thread = self.__create_thread(self.heartbeat, (delay, False))
            thread.start()

            return
        
        jitter = random.random()
        wait = round(delay/1000*jitter)
        time.sleep(wait)

        while self.open:
            self.send_json({
                "op": 1,
                "d": self.seq
            })

            time.sleep(delay/1000)

    def connect(self) -> None:
        self.open = True
        self.ws.connect(self.uri)

        self.heartbeat_interval = int(self.recv_json()["d"]["heartbeat_interval"])

    def identify(self, token) -> None:
        self.send_json({
            "op": 2,
            "d": {
                "token": token,
                "properties": {
                    "os": "Windows",
                    "os_version": "10",
                    "browser": "Chrome",
                    "device": "Desktop"
                }
            }
        })

    def listener(self, events: Union[str, list]) -> dict:
        if isinstance(events, str):
            events = [events]

        def decorator(callback):
            self.handlers.append({"callback": callback, "events": events})

        return decorator

    def listen(self, threaded=True) -> None:
        if threaded:
            thread = self.__create_thread(self.listen, (False,))
            thread.start()

            return
        
        last = None
        while True:
            data = self.recv_json()

            if data != last:
                if data:
                    self.seq = data["s"]

                    for handler in self.handlers:
                        if data["t"] in handler["events"]:
                            handler["callback"](data)
                        elif "ALL" in handler["events"]:
                                handler["callback"](data)

                    last = data

    def __create_thread(self, f, a=()):
        return threading.Thread(target=f, args=a, daemon=True)
        
        