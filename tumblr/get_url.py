import requests as r
import xmltodict, re
import threading, queue
import json,sys

def tumblr(site, chunk, type, start):
	res = r.get('http://{}.tumblr.com/api/read?num={}&type={}&start={}'.format(site, chunk, type, start))
	
	return get_source(xmltodict.parse(res.content),type, start, chunk)
	
	
def get_source(data, type, start=0, chunk=0):
	posts = stack = []
	try:
		posts = data['tumblr']['posts']['post']
	except KeyError as e:
		print(e)
	
	try:
		if type == 'photo':
			for i, post in enumerate(posts):
				try:
					stack.append(post['photo-url'][0]['#text'])		
				except KeyError:
					continue

		if type == 'video':
			for i, post in enumerate(posts):
				try:
					url = post['video-player'][1]['#text']
				except KeyError:
					continue
				pattern = re.compile(r'[\S\s]*src="(\S*)" ')
				match = pattern.match(url)
				if match is not None:
					try:	
						stack.append(match.group(1))
					except IndexError as e:
						print(e)
	except TypeError as e:
		pass
	return stack

		
if __name__ == '__main__':
	t = tumblr('',20,'video',1)
	print(t)
