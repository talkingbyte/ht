import re
from resources.lib import api_list, videosOnServer, xbet
from resources.lib.custom_api import linkstock, keeplinks, vup


def addVideo(videos):
	links = []
	for i in videos:
		if re.search('server',i):
			links.append(i)
		elif re.search('vup', i):
			link = vup.get(i)
			api_list.menu(link)
		if re.search('filmytorrent', i):
			xbet.addSecondary(i)
		elif re.search('linkstock',i):
			linkstock.menu(i)
		elif re.search('keeplinks',i):
			keeplinks.menu(i)
	if len(links)>0:
		videosOnServer.menu(links)
