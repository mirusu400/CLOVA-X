# Naver Clova X Unofficial API


![clova-logo](./doc/clova-logo.png)

<a href="https://pypi.org/project/clovax/"><img alt="PyPI package" src="https://img.shields.io/badge/pypi-clovax-green"></a>

Unofficial API for Naver Clova X, a Korean AI LLM (Language Model) service.

## Install

```
pip install clovax
```

## Usage

```python
from clovax import ClovaX

c = ClovaX()
c.get_cookie("[Your netscape cookie file]")
log = c.start("test")
print(log)
```

## How can I get cookie file?

1. Install [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
2. Export cookie
3. Set cookie file path to `get_cookie` function


## TODO

* [ ] Login using given naver ID and password
* [ ] Get existed conversation using conversation ID
* [ ] Proxy support
* [ ] Support personas

