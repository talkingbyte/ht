from xbmcaddon import Addon
import requests
import xbmc
import xbmcgui
import os
import re
from resources.lib import extractMY, dbHelper

ADDON = Addon(id='plugin.video.multiplex')
api_key = '01aa40b064d705f0b7a530f5df35b2b4'
fetch_info = ADDON.getSetting("fetch_info")
thumb = 'https://image.tmdb.org/t/p/w154'
icon = 'https://image.tmdb.org/t/p/w185'
full = 'https://image.tmdb.org/t/p/w780'
iconFile = 'DefaultVideo.png'
bgFile = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.multiplex/resources','fanart.jpg'))
	

def get(movie):
	title = movie['name']
	year = movie['year']
	if re.search('s\d',title):
		stype = 'tv'
	else:
		stype = 'movie'
	response = requests.get('https://api.themoviedb.org/3/search/{}?api_key={}&query={}&year={}'.format(stype,api_key,re.sub('s\d','',title),year))
	data = response.json()
	if data['results'] == []:
		dbHelper.insertInfo('',title, year, iconFile, bgFile, 'Plot Not Availble', '','','','','','','','','',0)
		####################id,name,year,poster,backdrop,plot,trailer,crew,tagline,genres,director,writer,release_date,mpaa,rating,duration
	else:
		info = data['results'][0]
		if not info['poster_path']:
			info['poster_path'] = ''
		if not info['backdrop_path']:
			info['backdrop_path'] = ''
		if not info.has_key('release_date'):
			info['release_date'] = info['first_air_date']
		response = requests.get('https://api.themoviedb.org/3/{}/{}?api_key={}&append_to_response=credits,videos,release_dates'.format(stype,info['id'],api_key))
		moreInfo = response.json()
		if moreInfo['videos']['results'] == []:
			ytt = ''
		else:
			ytt = moreInfo['videos']['results'][0]['key']
		if not 'credits' in moreInfo:
			casts = ''
			director  = ''
			writer = ''
		else:
			#casts = str(','.join(actor['name'].encode('utf-8') for actor in moreInfo['credits']['cast']))
			casts = [{'name': actor['name'].encode('utf-8'), 'role': actor['character'].encode('utf-8'), 'thumbnail': '{}{}'.format(icon,actor['profile_path'])} for actor in moreInfo['credits']['cast']]
			director = [w['name'] for w in moreInfo['credits']['crew'] if w['job'] == 'Director']
			writer = [w['name'] for w in moreInfo['credits']['crew'] if w['job'] == 'Story']
		if not moreInfo.has_key('tagline'):
			moreInfo['tagline'] = ''
		if not moreInfo.has_key('genres'):
			genres = ''
		else:
			genres = [genre['name'] for genre in moreInfo['genres']]
		try:
			mpaa = [country['release_dates'][0]['certification'] for country in moreInfo['release_dates']['results'] if country['iso_3166_1'] == 'US' or country['iso_3166_1'] == 'IN'][0]
			duration = moreInfo['runtime']*60
		except:
			mpaa = ''
			duration = 0
		dbHelper.insertInfo(info['id'],
							title,
							year,
							info['poster_path'],
							info['backdrop_path'],
							info['overview'],
							ytt,
							casts,
							moreInfo['tagline'],
							genres,
							director,
							writer,
							info['release_date'],
							mpaa,
							info['vote_average'],
							duration)

