import requests
import sys
import os
import re
import time
import xbmc
import xbmcgui
import xbmcaddon
from resources.lib import dbHelper
from urlparse import parse_qsl
from resources.lib.custom_api import desiupload,bdupload, indishare
import threading

addon = xbmcaddon.Addon(id='plugin.video.multiplex')


def stopMessage():
	xbmcgui.Window(10000).setProperty('cancel', 'true')


def msgSuccess(filename):
	xbmc.executebuiltin('Notification(Important,%s has been downloaded successfully,1000)'%(filename))
	dbHelper.remove(filename)	


def createVideo():
	thread = threading.Thread(target=download)
	thread.start()
	time.sleep(5)


def download():
	info = dict(parse_qsl(sys.argv[2][1:]))	
	link = info['action']
	if re.search('bdupload',link):
		link = bdupload.get(link)
	elif re.search('desiupload',link):
		link = desiupload.get(link)
	elif re.search('indishare',link):
		link = indishare.get(link)
	chunk_size = 4096
	download_path = addon.getSetting("download_path")
	filename = os.path.join(download_path,info['filename'])
	dp =xbmcgui.DialogProgressBG()
	if os.path.exists(filename):
		existSize = os.path.getsize(filename)
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 'Range': 'bytes=%d-' %(existSize)}
		f_mode = 'ab'
		dl = existSize
	else:
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
		f_mode = 'wb'
		dl = 0
	start = time.time()
	r = requests.get(link, allow_redirects=True, headers = headers, stream=True)
	r1 = requests.get(link, allow_redirects=True, stream=True)
	file_bytes = r1.headers.get('content-length')
	
	#database method
	if not dbHelper.available(info['filename']):
		dbHelper.add(info['filename'], info['action'], file_bytes)


######If the server doesn't provide file size######
	if file_bytes == None:
		with open(filename, f_mode) as f:
			for chunk in r.iter_content(chunk_size=chunk_size):
				if xbmcgui.Window(10000).getProperty('cancel') == 'true':
					xbmcgui.Window(10000).setProperty('cancel', 'false')
					return
				f.write(chunk)
		msgSuccess(info['filename'])
		return
		
	
	if dl == file_bytes:
		msgSuccess(info['filename'])
	
	else:
		file_mbytes = long(file_bytes)/(1024*1024)
		dp.create('Downloading','{} {}MB'.format(info['filename'], file_mbytes))
		data = 0
		with open(filename, f_mode) as f:	
			for chunk in r.iter_content(chunk_size=chunk_size):
				if xbmcgui.Window(10000).getProperty('cancel') == 'true':
					xbmcgui.Window(10000).setProperty('cancel', 'false')
					return
			
				dl += len(chunk)
				data += len(chunk)
				f.write(chunk)
				speed = int((data/(time.time() - start))/1000)
				if speed >= 1000:
					speed = speed/1000
					dl_rate = '{} MB/s'.format(speed)
				else:
					dl_rate = '{} KB/s'.format(speed)
				done = (100 * dl) / long(file_bytes)				
				dp.update(done, dl_rate)

			dp.close()
			msgSuccess(info['filename'])
