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
			if chunk == 1:
				stack.append(posts['photo-url'][0]['#text'])
			else:
				for i, post in enumerate(posts):
					stack.append(post['photo-url'][0]['#text'])		

		if type == 'video':
			if chunk == 1:
				url = posts['video-player'][1]['#text']
				pattern = re.compile(r'[\S\s]*src="(\S*)" ')
				match = pattern.match(url)
				if match is not None:
					try:
						stack.append(match.group(1))
					except IndexError as e:
						print(e)
			else:
				for i, post in enumerate(posts):
					url = post['video-player'][1]['#text']
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
	tumblr('mobpsycho100',30,'video',1)
