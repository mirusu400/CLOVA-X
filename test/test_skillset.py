from clovax import ClovaX
import json

c = ClovaX()
c.get_cookie("clova-x.naver.com_cookies.txt")
log = c.start("가을에 입을만한 바지 추천해 줘", skillsets=["shopping", "travel"])
print(log["text"])
with open("./test.html", "w", encoding="utf-8") as f:
    f.write(log["contents"][1]["content"])
