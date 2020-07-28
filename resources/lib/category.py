import requests
import xbmcgui
from bs4 import BeautifulSoup
from xbmcaddon import Addon
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

ADDON = Addon(id='plugin.video.multiplex')
main_url = ADDON.getSetting("main_url")


def parse(url):
	try:
		url = url.replace('{}{}'.format(main_url,main_url), main_url)
		r = requests.get(url.replace('file','server'))
	except requests.exceptions.ConnectionError as e:
		dialog = xbmcgui.Dialog()
		dialog.ok("[COLOR red][U]Network Issue[/U][/COLOR]","[COLOR yellow]Temporary Not Availabe[/COLOR]")
		raise SystemExit(e)	
	soup = BeautifulSoup(r.content, 'html.parser')
	return(soup)


def boomer(urls):
	movie = []
	with ThreadPoolExecutor(max_workers=100) as pool:
		future_results = [pool.submit(parse, '{}{}'.format(main_url,url)) for url in urls]
		concurrent.futures.wait(future_results)
	for future in future_results:
		movie.append(future.result())
	return movie



def parse_level(url):
	links = parse_first_level(url)
	soups = boomer(links)
	for soup in soups:
		for d in soup.select(".movie a"):
			yield d["href"]



def parse_first_level(url):
	soup = parse(url)
	for d in soup.select(".movie a"):
		yield d["href"]


def parse_second_level(url):
	soup = parse(url)
	for d in soup.select(".filedown a"):
		yield d["href"]


def parse_third_level(url):
	soup = parse(url)
	for d in soup.select(".movies a"):
		yield d["href"]


def parse_dailyupdate():
	soup = parse(main_url)
	cat = soup.select(".dailyupdate a")
	for i in range(len(cat)):
		if i % 2 != 0:
			yield cat[i]['href']
