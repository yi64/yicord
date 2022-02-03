from typing import Union

import requests

class User(object):
    def __init__(self) -> None:
        self.token: Union[str, None] = None
        self.info: Union[dict, None] = None
        self.api: int = 9

        self.session: requests.Session = requests.Session()

    def identify(self, token) -> bool:
        headers = {
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9003 Chrome/91.0.4472.164 Electron/13.4.0 Safari/537.36",
            "authorization": token
        }

        me = self.session.request(
            method="GET",
            url=f"https://discord.com/api/v{self.api}/users/@me",
            headers=headers
        )

        if me.status_code == 401:
            return False

        else:
            self.info = me.json()
            self.token = token
            self.session.headers.update(headers)

            return True
        
