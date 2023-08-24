# Naver Clova X Unofficial API


![clova-logo](./doc/clova-logo.png)

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
log = c.start("test")
print(log)
```

**Continue a conversation**
```python
from clovax import ClovaX

c = ClovaX()
c.get_cookie("[Your netscape cookie file]")
log = c.start("test", "안녕")
log = c.continue_conversation("test", "오늘 저녁 알려줘")
print(log)
```



## TODO

* [ ] Login using given naver ID and password
* [ ] Get existed conversation using conversation ID
* [ ] Proxy support
* [ ] Support personas

