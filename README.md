# Naver Clova X Unofficial API


![clova-logo](https://raw.githubusercontent.com/mirusu400/CLOVA-X/main/doc/clova-logo.png)

<a href="https://pypi.org/project/clovax/"><img alt="PyPI package" src="https://img.shields.io/badge/pypi-clovax-green"></a>
<a href="https://github.com/mirusu400/CLOVA-X/stargazers"><img src="https://img.shields.io/github/stars/mirusu400/CLOVA-X?style=social"></a>
<a href="https://pypi.org/project/clovax/"><img alt="PyPI" src="https://img.shields.io/pypi/v/clovax"></a>

Unofficial API for Naver Clova X, a Korean AI LLM (Language Model) service.

## Install

```
pip install clovax
```

## How can I get cookie file?

1. Install [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
2. Export cookie
3. Set cookie file path to `get_cookie` function

## Usage
**Start a conversation**
```python
from clovax import ClovaX

c = ClovaX()
c.get_cookie("[Your netscape cookie file]")
log = c.start("Hello world!")
print(log["text"])
```

**Continue a conversation**
```python
from clovax import ClovaX

c = ClovaX()
c.get_cookie("[Your netscape cookie file]")
log = c.start("Hello world!")
print(log["text"])
# At this time, you can continue the conversation using existed session (conversation ID)
log = c.conversation("Who are you?")
print(log["text"])
```

**Regenerate a conversation**
```python
from clovax import ClovaX

c = ClovaX()
c.get_cookie("[Your netscape cookie file]")
log = c.start("Hello world!")
log = c.regenerate()
print(log["text"])
```

**Conversation with a skillset**
```python
from clovax import ClovaX
import json

c = ClovaX()
c.get_cookie("clova-x.naver.com_cookies.txt")
log = c.start("가을에 입을만한 바지 추천해 줘", skillsets=["shopping", "travel"])
with open("./test.html", "w", encoding="utf-8") as f:
    f.write(log["contents"][1]["content"])
print(log["text"])
```




## TODO

* [ ] Login using given naver ID and password
* [ ] Get existed conversation using conversation ID
* [ ] Proxy support
* [ ] Support personas

