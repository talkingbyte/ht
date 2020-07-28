import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
from xbmcaddon import Addon
from resources.lib import get_url, dbHelper, extractMY
from urlparse import parse_qsl
import re
import json

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
settings = Addon(id='plugin.video.multiplex')
main_url = settings.getSetting("main_url")
download_path = settings.getSetting("download_path")
icon = 'https://image.tmdb.org/t/p/w185'
full = 'https://image.tmdb.org/t/p/w780'
bgFile = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.multiplex/resources','fanart.jpg'))



def menu(links):
	params = dict(parse_qsl(sys.argv[2][1:]))
	fname = params['filename']
	if os.path.exists(os.path.join(download_path,fname)):
		dl_context = 'Resume'
	else:
		dl_context = 'Download'
	for link in links:
		li = xbmcgui.ListItem(label="[COLOR yellow]Stream Now[/COLOR]")
		url = get_url.fetch(mode = 'video' ,filename = fname, action = main_url+link)
		myMovie = extractMY.extract(fname)
		movie = myMovie['name']
		year = myMovie['year']	
		tmdb = dbHelper.getInfo(movie, year)[0]

		if tmdb[1] == '':
			li.setArt({'icon': 'DefaultVideo.png',
					   'poster': 'DefaultVideo.png'})
		else:
			li.setArt({'icon': '{}{}'.format(icon,tmdb[1]),
					   'poster': '{}{}'.format(icon,tmdb[1])})
		if tmdb[2] == '':
			li.setArt({'fanart': bgFile})
		else:
			li.setArt({'fanart': '{}{}'.format(full,tmdb[2])})	
			
		if tmdb[5] == '':
			li.setInfo('video',{'cast': []})
		else:
			act = """{}""".format(tmdb[5])
			crew = list(json.loads(act))
			li.setCast(crew)
	
		tmp_genre = """{}""".format(tmdb[7])
		genre = list(json.loads(tmp_genre))
		
		tmp_director = """{}""".format(tmdb[8])
		director = list(json.loads(tmp_director))
		
		tmp_writer = """{}""".format(tmdb[9])
		writer = list(json.loads(tmp_writer))	
	
		li.setInfo('video',
			      {'title': movie,
			       'mediatype': 'movie',
			       'plot': tmdb[3],
			       'trailer': 'plugin://plugin.video.youtube/?action=play_video&videoid=%s'%tmdb[4],
			       'tagline': tmdb[6],
			       'genre': genre,
			       'director': director,
			       'writer': writer,
			       'aired': tmdb[10],
			       'mpaa': tmdb[11],
			       'rating': tmdb[12],
			       'duration': int(tmdb[13])})

		li.addContextMenuItems([(dl_context, 'xbmc.RunPlugin(%s?mode=download&filename=%s&action=%s)' %(base_url, fname, main_url+link))])
		li.setProperty('IsPlayable', 'true')
		#li.setIsFolder(False)
		xbmcplugin.addDirectoryItem(addon_handle, url, li, False)
	xbmcplugin.endOfDirectory(addon_handle)
