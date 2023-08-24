from clovax import ClovaX

c = ClovaX()
c.get_cookie("clova-x.naver.com_cookies.txt")
log = c.start("Hello world!")
print(log)
