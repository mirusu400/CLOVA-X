import requests
import json
import os.path
import random
import string
from typing import Union


class ClovaX:
    def __init__(
        self,
        NID_SES: Union[str, None] = None,
        NID_AUT: Union[str, None] = None,
        CVX_SES: Union[str, None] = None,
    ):
        self.NID_SES = NID_SES
        self.NID_AUT = NID_AUT
        self.CVX_SES = CVX_SES
        self.boundary = "".join(
            random.choice(string.ascii_lowercase + string.digits) for _ in range(16)
        )
        self.headers = {
            "accept": "*/*, text/event-stream",
            "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,und;q=0.6,zh-CN;q=0.5,zh;q=0.4",
            "baggage": "sentry-environment=prod,sentry-release=chat-fe-20230824,sentry-public_key=d2d631d03d52476e9f5553a10b361e93,sentry-trace_id=5c69173523314888b6cb3e2a69ac7050",
            "cache-control": "no-cache",
            "content-type": "multipart/form-data; boundary=----WebKitFormBoundary%s"
            % self.boundary,
            "pragma": "no-cache",
            "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "referer": "https://clova-x.naver.com/",
            "Origin": "https://clova-x.naver.com",
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        }
        self.session = requests.Session()
        self.conversation_id = ""
        self.turn_id = ""

    def get_cookie(self, cookie_file_src: str) -> None:
        """
        Get cookie from netscape cookie file.

        """
        if not os.path.exists(cookie_file_src):
            raise FileNotFoundError("Cookie file not found.")

        with open(cookie_file_src, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    domain, flag, path, secure, expiration, name, value = line.split(
                        "\t"
                    )
                    if name == "NID_AUT":
                        self.NID_AUT = value
                    elif name == "NID_SES":
                        self.NID_SES = value
                    elif name == "CVX_SES":
                        self.CVX_SES = value
        return

    def _build_data(self, text: str, action: str) -> str:
        """
        Build multipart/form-data.
        """

        data = (
            '------WebKitFormBoundary%s\r\nContent-Disposition: form-data; name="form"; filename="blob"\r\nContent-Type: application/json\r\n\r\n{"text":"%s","action":"%s"}\r\n------WebKitFormBoundary%s--\r\n'
            % (
                self.boundary,
                text,
                action,
                self.boundary,
            )
        )
        return data.encode()

    def _init_session(self) -> None:
        self.session.headers.update(self.headers)
        self.session.cookies.update(
            {
                "NID_SES": self.NID_SES,
                "NID_AUT": self.NID_AUT,
                "CVX_SES": self.CVX_SES,
            }
        )

    def start(self, prompt: str) -> dict:
        """
        Start conversation.

        Parameters:
            prompt (str): Prompt text.

        Returns:
            dict: Conversation data.
        """

        self._init_session()
        data = self._build_data(prompt, "new")
        r = self.session.post(
            "https://clova-x.naver.com/api/v1/generate",
            data=data,
            stream=True,
        )
        self.conversation_id = ""
        if r.status_code != 200:
            raise Exception("Error occurred while starting conversation.")

        # Iterate event stream, get event and datas
        for line in r.iter_lines(decode_unicode=True):
            if not line:
                continue

            if line.startswith("data:"):
                data = line[5:]
                if data == "{}":
                    continue

                try:
                    data = json.loads(line[5:])
                except json.decoder.JSONDecodeError:
                    continue

                if "conversationId" in data:
                    self.conversation_id = data["conversationId"]

            if line.startswith("event:"):
                event = line[6:]
                if event == "result":
                    r.close()
                    break

        r = self.session.get(
            f"https://clova-x.naver.com/api/v1/conversation/{self.conversation_id}",
        )

        return r.json()
