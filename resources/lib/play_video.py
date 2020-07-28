import sys
import xbmcgui
import xbmcplugin
from xbmcaddon import Addon
from resources.lib import downloadlink
from urlparse import parse_qsl

ADDON = Addon(id='plugin.video.multiplex')
addon_handle = int(sys.argv[1])

def play(path):
	play_item = xbmcgui.ListItem(path=path)
	xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)



def play2():
	info = dict(parse_qsl(sys.argv[2][1:]))
	ADDON.setSetting('cancel', 'false')
	downloadlink.createVideo()
	play_item = xbmcgui.ListItem(path=info['filepath'])
	xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
