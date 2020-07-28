import re
import requests
from bs4 import BeautifulSoup

def get(url):
	id = re.split('/',url)[-1]
	api_url = 'https://desiupload.co/f/woqliv-lhuehz4elym4n'
	data = {'op': 'download2', 'id': id, 'rand': '', 'referer': '','method_free': '','method_premium': '','adblock_detected': 0}
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'}
	r = requests.post(api_url, headers= headers, data = data)
	soup = BeautifulSoup(r.content,'html.parser')
	try:
		link = soup.find("span", id="direct_link")("a")[0]["href"]
	except:
		link = url
	return link
