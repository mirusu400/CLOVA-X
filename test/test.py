from clovax import ClovaX
import json

c = ClovaX()
c.get_cookie("clova-x.naver.com_cookies.txt")
log = c.start("Hello world!")["text"]
log = c.conversation("Who are you?")["text"]
print(log)
log = c.regenerate()["text"]
print(log)
