import re
import requests
from bs4 import BeautifulSoup


def get(url):	
    sess = requests.Session()
    r = sess.get(url)
    soup = BeautifulSoup(r.content,'html.parser')
    l = [d for d in soup.select("script")]
    link = ''.join(re.split(',', (re.split('"',(re.split('{', str(l[22]))[2]))[1])))
    return(link.replace('.urlset','/.urlset'))

print(get('https://vup.to/gr9plmd6i4ji.html'))
