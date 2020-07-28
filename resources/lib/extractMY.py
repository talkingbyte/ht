import re

def getInfo(fulltext):
	path = fulltext
	if re.search('linkstock',fulltext):
		return ({'name': 'LinkStock', 'year': '', 'path': path})
	elif re.search('keeplinks',fulltext):
		return ({'name': 'KeepLinks', 'year': '', 'path': path})
	else:	
		try:
			text = fulltext		
			fulltext = re.split('/',fulltext)[3]
			if fulltext == 'movie':
				fulltext = re.split('/',text)[5]
			fulltext = fulltext.replace('-', ' ')
		except:
			pass
		if re.search('480p|720p|1080p',fulltext):
			if re.search('[(]',fulltext):
				x = re.split('[$(.*]',fulltext)
				y = re.split('[$).*]',x[1])
				movie = x[0].strip()
				year = y[0]
			else:
				if re.search('[12][09][0-9][0-9]', fulltext):
					x = re.split('[12][09][0-9][0-9]', fulltext)
					y = re.search('[12][09][0-9][0-9]', fulltext)
					movie = x[0].strip()
					year = y.group()			
				else:
					movie = fulltext
					year = ''	
		else:
			movie = fulltext
			year = ''
		return ({'name': movie,'year': year, 'path': path})


def extract(text):
	x = re.split('[$(.*]', text)
	y = re.split('[$).*]', x[1])
	movie = x[0].strip()
	year = y[0]
	return ({'name': movie,'year': year})

def quality(text):
	stream = ''
	if not re.search('(?=.*rl)(?=.*720p)(?=.*480p)(?=.*1080p)|(?=.*720p)(?=.*480p)|(?=.*720p)(?=.*480p)(?=.*1080p)',text):
		if re.search('rl', text):
			stream = 'RL'
		elif re.search('480p', text):
			stream = '480p'
		elif re.search('720p', text):
			stream = '720p'
		elif re.search('1080p', text):
			stream = '1080p'
	return (stream)
