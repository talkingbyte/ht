import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
from xbmcaddon import Addon
from resources.lib import get_url, metaInfo, extractMY, dbHelper
import re
import json


ADDON = Addon(id='plugin.video.multiplex')
ADDON_PATH = ADDON.getAddonInfo("path")
addon_handle = int(sys.argv[1])
base_url = sys.argv[0]
download_path = ADDON.getSetting("download_path")
icon = 'https://image.tmdb.org/t/p/w185'
full = 'https://image.tmdb.org/t/p/w780'
bgFile = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.multiplex/resources','fanart.jpg'))


def menu():
	"""
	Creating a listing for Current Downloads.
	
	"""
	listing = dbHelper.show()
	for item in listing:
		download = extractMY.extract(item[0])
		movie = download['name']
		year = download['year']
		link = item[1]
		
		videoPath = os.path.join(download_path, item[0])
		li = xbmcgui.ListItem('[COLOR green]%s[/COLOR]'%(movie))
		li.setInfo('video', {'title': movie, 'mediatype': 'movies'})
		li.addContextMenuItems([('Resume Download', 'xbmc.RunPlugin(%s?mode=download&filename=%s&action=%s)' %(base_url, item[0], item[1])),
								('STOP', 'xbmc.RunPlugin(%s?mode=stop)' %(base_url)),
								('Remove', 'xbmc.RunPlugin(%s?mode=remove&filename=%s)' %(base_url, item[0]))])
		url = get_url.fetch(mode='video', action=videoPath)
		#li.setIsFolder(False)
		li.setProperty('IsPlayable', 'true')
		xbmcplugin.addDirectoryItem(addon_handle,url,li,False)
	xbmcplugin.endOfDirectory(addon_handle)
