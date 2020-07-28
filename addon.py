import sys
import re
import xbmcgui
from xbmcaddon import Addon
from urlparse import parse_qsl
from resources.lib import navigator, category, play_video, downloadlink, download_list, dbHelper, first_level, second_level, third_level, xbet
from resources.lib.custom_api import linkstock, keeplinks

ADDON = Addon(id='plugin.video.multiplex')
main_url = ADDON.getSetting("main_url")
xbetmovies = ADDON.getSetting("xbetmovies")


def router(paramstring):
	params = dict(parse_qsl(paramstring))
	
	if params:
		if params['mode'] == 'main':
			navigator.getSubMenu(params['category'])
		elif params['mode'] == 'first_level':
			feeder = params['action']
			URLS = category.parse_first_level(feeder)
			first_level.addDir(URLS)
		elif params['mode'] == 'second_level':
			feeder = params['action']
			URLS = category.parse_second_level(feeder)
			second_level.addDir(URLS)
		elif params['mode'] == 'third_level':
			feeder = params['action']
			if re.search('linkstock', feeder):
				third_level.addVideo(feeder)
			else:
				URLS = category.parse_third_level(feeder)
				third_level.addVideo(URLS)
		elif params['mode'] == 'page':
			first_level.addPages()
		elif params['mode'] == 'dailyupdate':
			first_level.addDir(category.parse_dailyupdate())
		elif params['mode'] == 'xbet':
			xbet.addPrimary(xbetmovies)
		elif params['mode'] == 'xbetpage':
			xbet.addPrimary(params['link'])
		elif params['mode'] == 'xbetAgain':
			xbet.addSecondary(params['link'])
		elif params['mode'] == 'linkstock':
			linkstock.menu(params['link'])
		elif params['mode'] == 'video':
			play_video.play(params['action'])
		elif params['mode'] == 'altvideo':
			play_video.play2()
		elif params['mode'] == 'download':
			downloadlink.download()
		elif params['mode'] == 'stop':
			downloadlink.stopMessage()
		elif params['mode'] == 'check download':
			download_list.menu()
		elif params['mode'] == 'remove':
			dbHelper.remove(params['filename'])
		else:
			raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
	else:
		navigator.getMainMenu()

if __name__ == '__main__':
	router(sys.argv[2][1:])
