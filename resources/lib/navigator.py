import os
import sys
import xbmc
import xbmcgui
from xbmcaddon import Addon
import xbmcplugin
from urlparse import parse_qsl
from resources.lib import get_url, category, first_level


ADDON = Addon(id='plugin.video.multiplex')
main_url = ADDON.getSetting("main_url")
base = '{}/category/'.format(main_url)
addon_handle = int(sys.argv[1])
base_url = sys.argv[0]
imgPath = xbmc.translatePath('special://home/addons/plugin.video.multiplex/resources/media')
uncut = xbmc.translatePath('special://home/addons/plugin.video.multiplex/.uncut')

listing = {'Bollywood': [{'name': '2020', 'link': '{}522/Latest-bollywood-movies-(2020)/default/1.html'.format(base)},
					 {'name': '2019', 'link': '{}336/Latest-bollywood-movies-(2019)/default/1.html'.format(base)},
					 {'name': '2018', 'link': '{}257/Latest-bollywood-movies-(2018)/default/1.html'.format(base)},
					 {'name': '2017', 'link': '{}283/Latest-bollywood-movies-(2017)/default/1.html'.format(base)},
					 {'name': '2016', 'link': '{}284/Latest-bollywood-movies-(2016)/default/1.html'.format(base)},
					 {'name': '2015', 'link': '{}285/Latest-bollywood-movies-(2015)/default/1.html'.format(base)},
					 {'name': '2014', 'link': '{}286/Latest-bollywood-movies-(2014)/default/1.html'.format(base)},
					 {'name': '2013', 'link': '{}287/Latest-bollywood-movies-(2013)/default/1.html'.format(base)},
					 {'name': '2012', 'link': '{}288/Latest-bollywood-movies-(2012)/default/1.html'.format(base)},
					 {'name': '2011', 'link': '{}289/Latest-bollywood-movies-(2011)/default/1.html'.format(base)},
					 {'name': 'Older', 'link': '{}261/Bollywood-old-movies/default/1.html'.format(base)}],
		   'Hollywood': [{'name': '2020', 'link': '{}539/Latest-hollywood-movies-(2020)/default/1.html'.format(base)},
					 {'name': '2019', 'link': '{}337/Latest-hollywood-movies-(2019)/default/1.html'.format(base)},
					 {'name': '2018', 'link': '{}291/Latest-hollywood-movies-(2018)/default/1.html'.format(base)},
					 {'name': '2017', 'link': '{}292/Latest-hollywood-movies-(2017)/default/1.html'.format(base)},
					 {'name': '2016', 'link': '{}293/Latest-hollywood-movies-(2016)/default/1.html'.format(base)},
					 {'name': 'Older', 'link': '{}294/Latest-hollywood-old-movies-/default/1.html'.format(base)}],
		   'Dual Audio': [{'name': '2020', 'link': '{}532/Latest-hollywood-dual-audio-movies-(2020)/default/1.html'.format(base)},
					{'name': '2019', 'link': '{}342/Latest-hollywood-dual-audio-movies-(2019)/default/1.html'.format(base)},
					{'name': '2018', 'link': '{}273/Latest-hollywood-dual-audio-movies-(2018)/default/1.html'.format(base)},
					{'name': '2017', 'link': '{}274/Latest-hollywood-dual-audio-movies-(2017)/default/1.html'.format(base)},
					{'name': '2016', 'link': '{}275/Latest-hollywood-dual-audio-movies-(2016)/default/1.html'.format(base)},
					{'name': '2015', 'link': '{}276/Latest-hollywood-dual-audio-movies-(2015)/default/1.html'.format(base)},
					{'name': '2014', 'link': '{}277/Latest-hollywood-dual-audio-movies-(2014)/default/1.html'.format(base)},
					{'name': '2013', 'link': '{}278/Latest-hollywood-dual-audio-movies-(2013)/default/1.html'.format(base)},
					{'name': '2012', 'link': '{}279/Latest-hollywood-dual-audio-movies-(2012)/default/1.html'.format(base)},
					{'name': '2011', 'link': '{}280/Latest-hollywood-dual-audio-movies-(2011)/default/1.html'.format(base)},
					{'name': '2010', 'link': '{}281/Latest-hollywood-dual-audio-movies-(2010)/default/1.html'.format(base)},
					{'name': 'Older', 'link': '{}282/Latest-hollywood-dual-audio-movies/default/1.html'.format(base)}],
		   'Series': '{}262/Series-film-lists/default/1.html'.format(base),
		   'South Dubbed': [{'name': '2020', 'link': '{}525/Latest-south-indian-hindi-dubbed-movies-(2020)/default/1.html'.format(base)},
					 {'name': '2019', 'link': '{}335/Latest-south-indian-hindi-dubbed-movies-(2019)/default/1.html'.format(base)},
					 {'name': '2018', 'link': '{}295/Latest-south-indian-hindi-dubbed-movies-(2018)/default/1.html'.format(base)},
					 {'name': '2017', 'link': '{}296/Latest-south-indian-hindi-dubbed-movies-(2017)/default/1.html'.format(base)},
					 {'name': '2016', 'link': '{}297/Latest-south-indian-hindi-dubbed-movies-(2016)/default/1.html'.format(base)},
					 {'name': '2015', 'link': '{}298/Latest-south-indian-hindi-dubbed-movies-(2015)/default/1.html'.format(base)},
					 {'name': 'Older', 'link': '{}302/Latest-south-indian-hindi-dubbed-movies-/default/1.html'.format(base)}],
		   'TV Shows': '{}270/Indian-tv-shows-/default/1.html'.format(base)}

	
def subListing(cat):
	return listing[cat]

def mainListing():
	return listing.iterkeys()
	
def getSubMenu(cat):
	items = subListing(cat)
	if type(items) == str:
		URLS = category.parse_level(items)
		first_level.addDir(URLS)
	else:	
		for item in items:
			li = xbmcgui.ListItem(label="[COLOR yellow]%s[/COLOR]"%item['name'])
			url = get_url.fetch(mode='first_level', action=item['link'])
			li.setIsFolder(True)
			xbmcplugin.addDirectoryItem(addon_handle, url, li, True)
		xbmcplugin.endOfDirectory(addon_handle)		


def getMainMenu():
	
	if os.path.exists(uncut):
		li_daily = xbmcgui.ListItem('[COLOR green]RECENTLY ADDED[/COLOR]')
		url = get_url.fetch(mode = 'dailyupdate' , action = main_url)
		li_daily.setIsFolder(True)
		xbmcplugin.addDirectoryItem(addon_handle,url,li_daily,True)
	
		
		li_1xbet = xbmcgui.ListItem('[COLOR white]NEW & POPULAR[/COLOR]')
		url = get_url.fetch(mode = 'xbet')
		li_1xbet.setArt({'poster': '{}/New.png'.format(imgPath)})
		li_1xbet.setIsFolder(True)
		xbmcplugin.addDirectoryItem(addon_handle,url,li_1xbet,True)
	
	
	li_download = xbmcgui.ListItem('[COLOR green]DOWNLOADS[/COLOR]')
	url = get_url.fetch(mode = 'check download')
	li_download.setArt({'poster': '{}/Download.png'.format(imgPath)})
	li_download.setIsFolder(True)
	xbmcplugin.addDirectoryItem(addon_handle,url,li_download,True)
	
	menu = mainListing()
	for cat in menu:
		li = xbmcgui.ListItem(label="[COLOR yellow]%s[/COLOR]"%cat)
		url = get_url.fetch(mode='main', category=cat)
		li.setArt({'poster': '{}/{}.png'.format(imgPath, cat)})
		li.setIsFolder(True)
		xbmcplugin.addDirectoryItem(addon_handle, url, li, True)
	xbmcplugin.endOfDirectory(addon_handle)	

	
