import os
import sqlite3
from sqlite3 import Error

def delMeta():
	con = None
	try:
		con = sqlite3.connect(os.path.join('/home/pi/.kodi/addons/plugin.video.multiplex/resources/data','data.db'))
		cursor = con.cursor()
		cursor.execute("DELETE FROM meta;")
		con.commit()
		#cursor.execute("SELECT name, year FROM meta WHERE name LIKE'%{}';".format(movie))
		data = cursor.fetchall()
		print(len(data))
		#for d in data:
			#print(d)
	except Error as e:
		print(e)
	finally:
		if con:
			con.close()
delMeta()
