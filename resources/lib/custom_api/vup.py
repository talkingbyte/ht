import re
import requests
from bs4 import BeautifulSoup


def get(url):	
    sess = requests.Session()
    r = sess.get(url)
    soup = BeautifulSoup(r.content,'html.parser')
    l = [d.get_text() for d in soup.select("script")][20]
    m = re.split("\|", l)
    if m[len(m)-10] == "urlset":
        return("https://{}.{}.to/{}/{}/urlset/master.m3u8".format(m[len(m)-6], m[len(m)-7], m[len(m)-8], m[len(m)-9]))
    else:
        return("https://{}.{}.to/{}/{}{}{}/urlset/master.m3u8".format(m[len(m)-6], m[len(m)-7], m[len(m)-8], m[len(m)-9], m[len(m)-10], m[len(m)-11]))

#print(get('https://vup.to/gr9plmd6i4ji.html'))
#print(get('https://vup.to/3ec5db98pa4n.html'))

