import re
import requests
from bs4 import BeautifulSoup

def get(url):
	id = re.split('/',url)[-1]
	api_url = 'https://bdupload.asia/' + id
	data = {'op': 'download2', 'id': id, 'rand': '', 'referer': '','method_free': '','method_premium': ''}
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'}
	r = requests.post(api_url, headers= headers, data = data)
	soup = BeautifulSoup(r.content,'html.parser')
	try:
		link = soup.find("a", class_="btn_gen")["href"]
	except:
		link = url
	return link
