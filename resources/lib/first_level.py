import re
import os
import sys
import json
import xbmc
import xbmcgui
import xbmcplugin
import pickle
from xbmcaddon import Addon
from urlparse import parse_qsl
from resources.lib import extractMY, get_url, metaInfo, dbHelper
from resources.lib.custom_api import linkstock, keeplinks
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

addon_handle = int(sys.argv[1])
ADDON = Addon(id='plugin.video.multiplex')
main_url = ADDON.getSetting("main_url")
icon = 'https://image.tmdb.org/t/p/w185'
full = 'https://image.tmdb.org/t/p/w780'
bgFile = xbmc.translatePath('special://home/addons/plugin.video.multiplex/resources/fanart.jpg')
pickledfile = xbmc.translatePath('special://home/addons/plugin.video.multiplex/resources/data/_p')

if ADDON.getSetting("items_per_page") == '':
	items_per_page  = 10
else:
	items_per_page  = int(ADDON.getSetting("items_per_page"))



def pagination(seq, rowlen):
	for start in xrange(0,len(seq), rowlen):
		yield seq[start:start+rowlen]


def movieList(urls):
	movie = []
	with ThreadPoolExecutor(max_workers=100) as pool:
		future_results = [pool.submit(extractMY.getInfo, url) for url in urls]
		concurrent.futures.wait(future_results)
	for future in future_results:
		movie.append(future.result())
	return movie



def infoList(movies):
	addInfo = []
	for movie in movies:
		if not dbHelper.infoAvailable(movie):
			addInfo.append(movie)
	with ThreadPoolExecutor(max_workers=len(addInfo)) as pool:
		future_info = [pool.submit(metaInfo.get, no_info) for no_info in addInfo]




def linksForPages():
	with open(pickledfile, 'rb') as f:
		return pickle.load(f)


	
def addPages():
	links = pagination(linksForPages(), items_per_page)
	URLS = []
	for link in links:
		URLS.append(link)
	params = dict(parse_qsl(sys.argv[2][1:]))
	if params.has_key('page'):
		page = int(params['page'])
	else:
		page = 1
	movies = movieList(URLS[page-1])
	infoList(movies)
	offset = 1
	listing = []
	#xbmc.log('total number of pages %s'%(str(len(movies))),xbmc.LOGNOTICE)
	for movie in movies:
		offset += 1
		if re.search('orgmovies', movie['path']):
			continue
		if re.search('linkstock', movie['path']):
			linkstock.menu(movie['path'])
		elif re.search('keeplinks', movie['path']):
			keeplinks.menu(movie['path'])
		else:
			tmdb = dbHelper.getInfo(movie['name'], movie['year'])[0]
			filename = '{} ({}).mkv'.format(movie['name'],movie['year'])
			url = get_url.fetch(mode = 'second_level' , action = '{}{}'.format(main_url,movie['path']), filename = filename)
			li = xbmcgui.ListItem(label='[COLOR golden]%s[/COLOR]'%movie['name'])
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
				      {'title': movie['name'],
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

			#li.setIsFolder(True)
			isFolder = True
			listing.append((url, li, isFolder))
	xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
	if offset > items_per_page:
		nextPage = xbmcgui.ListItem('[COLOR blue]Next Page[/COLOR]', iconImage='DefaultFolder.png')
		url = get_url.fetch(mode='page', page=page+1)
		#nextPage.setIsFolder(True)
		xbmcplugin.addDirectoryItem(addon_handle,url,nextPage,True)
	xbmcplugin.endOfDirectory(addon_handle)



def addDir(URLS):
	with open(pickledfile, 'wb') as f:
		pickle.dump([url for url in URLS], f)
	addPages()
	
