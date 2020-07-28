import os
import sqlite3
from sqlite3 import Error

def viewInfo():
	con = None
	try:
		con = sqlite3.connect(os.path.join('/home/pi/.kodi/addons/plugin.video.multiplex/resources','sample.db'))
		cursor = con.cursor()
		cursor.execute("SELECT * FROM folders;")
		data = cursor.fetchall()
		for eachData in data:
			print(eachData)
	except Error as e:
		print(e)
	finally:
		if con:
			con.close()


def addInfo(data):
	con = None
	try:
		con = sqlite3.connect(os.path.join('/home/pi/.kodi/addons/plugin.video.multiplex/resources','sample.db'))
		cursor = con.cursor()
		cursor.executemany("INSERT INTO folders(main) VALUES(?);",data)
		con.commit()
	except Error as e:
		print(e)
	finally:
		if con:
			con.close()

addInfo()		
viewInfo()
