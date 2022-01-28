from urllib.request import urlopen
import re

get_followers = lambda x:int(re.findall(r",\"edge_followed_by\":{\"count\":(\d+)},",str(urlopen(x).read(),"utf-8"),re.MULTILINE)[0])

print (get_followers("https://www.instagram.com/anton/"))
