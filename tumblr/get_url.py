import requests as r
import xmltodict, re
import threading, queue
import json	

def tumblr(site, chunk, type, start):
	res = r.get('http://{}.tumblr.com/api/read?num={}&type={}&start={}'.format(site, chunk, type, start))

	if type == 'photo':
		d = t_photo(xmltodict.parse(res.content), start, chunk)	
		for i in d:
			print(i)
	if type == 'video':
		d = t_video()
	
	
def t_photo(data, start=0, chunk=0):
	try:
		posts = data['tumblr']['posts']['post']
		print(len(posts))
		if chunk == 1:
			yield posts['photo-url'][0]['#text']
		else:
			for i, post in enumerate(posts):
				url = post['photo-url'][0]['#text']
				yield url
	except KeyError:
		pass

def t_video():
	pass
	
		
tumblr('mobpsycho100',1,'photo',1)

