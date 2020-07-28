import os
import sqlite3
from sqlite3 import Error

def view(movie):
	con = None
	try:
		con = sqlite3.connect(os.path.join('/home/pi/.kodi/addons/plugin.video.multiplex/resources/data','data.db'))
		cursor = con.cursor()
		cursor.execute("SELECT * FROM dl;")
		#cursor.execute("SELECT * FROM meta WHERE(name LIKE'%Doctor strange' AND year='2016');")
		#cursor.execute("SELECT name, year, poster, backdrop, plot FROM meta WHERE name LIKE'%{}';".format(movie))
		data = cursor.fetchall()
		print(len(data))
		for d in data:
			print(d)
	except Error as e:
		print(e)
	finally:
		if con:
			con.close()
view('Bollywood old movies')
