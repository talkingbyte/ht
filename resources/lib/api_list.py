import sys
import xbmc
import xbmcgui
import xbmcplugin
from urlparse import parse_qsl
from resources.lib import get_url, extractMY


addon_handle = int(sys.argv[1])


def menu(hoster):
	params = dict(parse_qsl(sys.argv[2][1:]))
	fname = params['filename']
	myMovie = extractMY.extract(fname)
	movie = myMovie['name']
	year = myMovie['year']
	#xbmc.log('Got %s from api_list'%(hoster),xbmc.LOGNOTICE)
	url = get_url.fetch(mode = 'video', filename = fname, action = hoster)
	li = xbmcgui.ListItem(label=movie)
	li.setInfo('video', {'title': movie, 'mediatype': 'movies'})
	li.setProperty('IsPlayable', 'true')
	#li.setIsFolder(False)
	xbmcplugin.addDirectoryItem(addon_handle, url, li, False)
	xbmcplugin.endOfDirectory(addon_handle)
