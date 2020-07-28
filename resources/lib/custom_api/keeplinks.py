import re
import requests
from bs4 import BeautifulSoup
from resources.lib import api_list
from resources.lib.custom_api import vup

def get(url):	
    sess = requests.Session()
    r = sess.get(url)
    soup = BeautifulSoup(r.content,'html.parser')
    token = soup.find('input')['value']		#_csrf_token_645a83a41868941e4692aa31e7235f2
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'}
    data = {'_csrf_token_645a83a41868941e4692aa31e7235f2': token}
    r = sess.post(r.url, headers= headers, data=data)
    soup = BeautifulSoup(r.content,'html.parser')
    l = [d['href'] for d in soup.select("div a")[4:-6:]]
    for x in l:
        yield x

def menu(url):
	links = get(url)
	for link in links:
		if re.search('vup',link):
			api_list.menu(vup.get(link))
