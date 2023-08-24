# Naver Clova X Unofficial API


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

### How can I get cookie file?
1. Install [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
2. Export cookie
3. Set cookie file path to `get_cookie` function