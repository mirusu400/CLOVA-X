import requests
import json
import os.path
import random
import string
import clovax.errors
from clovax.constants import AVAILABLE_SKILLSETS, AVAILABLE_SKILLSETS_LITERAL
from typing import Union, List


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
        self.conversation_id_history = []
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
                    parts = line.split("\t")

                    while len(parts) < 7:
                        parts.append("None")

                    domain, flag, path, secure, expiration, name, value = parts
                    if name == "NID_SES":
                        self.NID_SES = value
                    elif name == "NID_AUT":
                        self.NID_AUT = value
                    elif name == "CVX_SES":
                        self.CVX_SES = value
        return

    def _build_data(
        self,
        action: str,
        text: Union[str, None] = None,
        parent_turn_id: Union[str, None] = None,
        conversation_id: Union[str, None] = None,
        skillsets: List[AVAILABLE_SKILLSETS_LITERAL] = [],
    ) -> bytes:
        """
        Build multipart/form-data.
        """

        data = (
            '------WebKitFormBoundary%s\r\nContent-Disposition: form-data; name="form"; filename="blob"\r\nContent-Type: application/json\r\n\r\n'
            % self.boundary
        )

        data += '{"action": "%s"' % action

        if text:
            data += ',"text":"%s"' % text
        if parent_turn_id:
            data += ',"parentTurnId":"%s"' % parent_turn_id
        if conversation_id:
            data += ',"conversationId":"%s"' % conversation_id
        if len(skillsets) > 0:
            data += ',"skillSets":%s' % json.dumps(skillsets)

        data += "}\r\n------WebKitFormBoundary%s--\r\n" % self.boundary
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

    def _get_conversation(self, conversation_id: str) -> dict:
        r = self.session.get(
            f"https://clova-x.naver.com/api/v1/conversation/{conversation_id}",
        )
        return r.json()

    def _do_conversation(self, data: bytes) -> requests.Response:
        r = self.session.post(
            "https://clova-x.naver.com/api/v1/generate",
            data=data,
            stream=True,
        )

        if r.status_code != 200:
            if r.status_code == 401:
                raise clovax.errors.UnauthorizedError()
            elif r.status_code == 429:
                raise clovax.errors.TooManyRequestsError()
            else:
                raise Exception(
                    f"Error occurred while starting conversation. Error code: {r.status_code}, Error message: {r.text}"
                )
        r.encoding = "utf-8"
        return r

    def _parse_latest_data(self, conversation_data: dict) -> dict:
        latest_turn_id = conversation_data["path"][-1]
        latest_data = conversation_data["turnTree"][latest_turn_id]
        return latest_data["turn"]

    def _check_skillsets(self, skillsets: List[AVAILABLE_SKILLSETS_LITERAL]) -> bool:
        for skillset in skillsets:
            if skillset not in AVAILABLE_SKILLSETS:
                return False
        return True

    def start(
        self, prompt: str, skillsets: List[AVAILABLE_SKILLSETS_LITERAL] = []
    ) -> dict:
        """
        Start conversation.

        Parameters:
            prompt (str): Prompt text.

        Returns:
            dict: Conversation data.
        """
        if self.NID_SES is None or self.NID_AUT is None or self.CVX_SES is None:
            raise clovax.errors.NoTokenSetError()
        if not self._check_skillsets(skillsets):
            raise clovax.errors.InvalidSkillsetError()

        self._init_session()
        data = self._build_data("new", prompt, skillsets=skillsets)
        self.conversation_id = ""

        r = self._do_conversation(data)

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
                    self.conversation_id_history.append(self.conversation_id)

            if line.startswith("event:"):
                event = line[6:]
                if event == "result":
                    r.close()
                    break
        conversation_data = self._get_conversation(self.conversation_id)
        return self._parse_latest_data(conversation_data)

    def conversation(
        self,
        prompt: str,
        conversation_id: Union[str, None] = None,
        skillsets: List[AVAILABLE_SKILLSETS_LITERAL] = [],
    ) -> dict:
        if not self._check_skillsets(skillsets):
            raise clovax.errors.InvalidSkillsetError()
        if conversation_id:
            self.conversation_id = conversation_id

        conversation_data = self._get_conversation(self.conversation_id)
        self.turn_id = conversation_data["path"][-1]

        data = self._build_data(
            "generate",
            prompt,
            parent_turn_id=self.turn_id,
            conversation_id=self.conversation_id,
            skillsets=skillsets,
        )
        r = self._do_conversation(data)

        for line in r.iter_lines(decode_unicode=True):
            if not line:
                continue

            if line.startswith("event:"):
                event = line[6:]
                if event == "result":
                    r.close()
                    break

        conversation_data = self._get_conversation(self.conversation_id)
        return self._parse_latest_data(conversation_data)

    def regenerate(self, conversation_id: Union[str, None] = None):
        if conversation_id:
            self.conversation_id = conversation_id

        conversation_data = self._get_conversation(self.conversation_id)
        self.turn_id = conversation_data["path"][-1]

        data = self._build_data("regenerate", conversation_id=self.conversation_id)
        r = self._do_conversation(data)

        for line in r.iter_lines(decode_unicode=True):
            if not line:
                continue

            if line.startswith("event:"):
                event = line[6:]
                if event == "result":
                    r.close()
                    break

        conversation_data = self._get_conversation(self.conversation_id)
        return self._parse_latest_data(conversation_data)
