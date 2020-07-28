import os
import json
import xbmc
import sqlite3
from sqlite3 import Error


def insertInfo(tid,title,year,poster,backdrop,plot,trailer,casts, tagline, genres, director, writer, release_date, mpaa, rating, duration):
	con = None
	try:
		con = sqlite3.connect(xbmc.translatePath(os.path.join('special://home/addons/plugin.video.multiplex/resources/data','data.db')))
		cursor = con.cursor()
		cursor.execute("INSERT INTO meta(id, name, year, poster, backdrop, plot, trailer, crew, tagline, genres, director, writer, release_date, mpaa, rating, duration) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",(tid, title, year, poster, backdrop, plot, trailer, json.dumps(casts), tagline, json.dumps(genres), json.dumps(director), json.dumps(writer), release_date, mpaa, rating, duration))
		con.commit()
		#xbmc.log('%s has been inserted successfully.'%title,xbmc.LOGNOTICE)
	except Error as e:
		xbmc.log('Failed due to %s'%(e),xbmc.LOGERROR)
	finally:
		if con:
			con.close()

def getInfo(movie,year):
	con = None
	try:
		con = sqlite3.connect(xbmc.translatePath(os.path.join('special://home/addons/plugin.video.multiplex/resources/data','data.db')))
		cursor = con.cursor()
		cursor.execute("SELECT id, poster, backdrop, plot, trailer, crew, tagline, genres, director, writer, release_date, mpaa, rating, duration FROM meta WHERE name LIKE'%{}' AND year='{}';".format(movie,year))
		data = cursor.fetchall()
		#xbmc.log('Got %s for %s from dbHelper.getInfo'%(movie),xbmc.LOGNOTICE)
		return data
	except Error as e:
		#xbmc.log('%s'%e,xbmc.LOGERROR)
		xbmc.log('Unable to get Info for %s: %s'%(movie,e),xbmc.LOGERROR)
	finally:
		if con:
			con.close()
			

def infoAvailable(text):
	con = None
	try:
		movie = text['name']
		year = text['year']
		con = sqlite3.connect(xbmc.translatePath(os.path.join('special://home/addons/plugin.video.multiplex/resources/data','data.db')))
		cursor = con.cursor()
		cursor.execute("SELECT id FROM meta WHERE name LIKE'%{}' AND year='{}';".format(movie,year))
		data = cursor.fetchall()
		if len(data)>0:
			return True
		else:
			return False
	except Error as e:
		xbmc.log('Checking Failed due to %s'%e,xbmc.LOGERROR)
	finally:
		if con:
			con.close()			
			


def add(name,path,size):
	con = None
	try:
		con = sqlite3.connect(xbmc.translatePath(os.path.join('special://home/addons/plugin.video.multiplex/resources/data','data.db')))
		cursor = con.cursor()
		cursor.execute("INSERT INTO dl values(?,?,?);",(name,path,size))
		con.commit()
		#xbmc.log('Now, we can be download %s (%s) from %s'%(name,size,path),xbmc.LOGNOTICE)
	except Error as e:
		xbmc.log('%s'%e,xbmc.LOGERROR)
	finally:
		if con:
			con.close()
			
def show():
	con = None
	try:
		con = sqlite3.connect(xbmc.translatePath(os.path.join('special://home/addons/plugin.video.multiplex/resources/data','data.db')))
		cursor = con.cursor()
		cursor.execute("SELECT * FROM dl;")
		data = cursor.fetchall()
		return data
	except Error as e:
		xbmc.log('%s'%e,xbmc.LOGERROR)
	finally:
		if con:
			con.close()

def available(movie):
	con = None
	try:
		con = sqlite3.connect(xbmc.translatePath(os.path.join('special://home/addons/plugin.video.multiplex/resources/data','data.db')))
		cursor = con.cursor()
		cursor.execute("SELECT * FROM dl WHERE name LIKE'%{}';".format(movie))
		data = cursor.fetchall()
		if len(data) > 0:
			return True
		else:
			return False
	except Error as e:
		xbmc.log('%s'%e,xbmc.LOGERROR)
	finally:
		if con:
			con.close()	
	
			
def remove(movie):
	con = None
	try:
		con = sqlite3.connect(xbmc.translatePath(os.path.join('special://home/addons/plugin.video.multiplex/resources/data','data.db')))
		cursor = con.cursor()
		cursor.execute("DELETE FROM dl WHERE name LIKE'%{}';".format(movie))
		con.commit()
	except Error as e:
		xbmc.log('%s'%e,xbmc.LOGERROR)
	finally:
		if con:
			con.close()
	xbmc.executebuiltin('Container.Refresh')
