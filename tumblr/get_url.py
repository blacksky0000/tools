import requests as r
import xmltodict, re
import threading
import json,sys
from bs4 import BeautifulSoup
from urlparse import urlparse

def tumblr(site, chunk, type, start):
	res = r.get('http://{}.tumblr.com/api/read?num={}&type={}&start={}'.format(site, chunk, type, start))
	if res.status_code != r.codes.ok:
		print("[@] Request_code: {}, User not found.".format(res.status_code))
		sys.exit(1)

	dicts = xmltodict.parse(res.content)
	return get_redirect(dicts, type)
	# return get_source(dicts, type, start, chunk)

def get_redirect(data, type):
	try:
		html_list = data['tumblr']['posts']['post']
	except KeyError as e:
		print('[@] KeyError: {}'.format(e))
		sys.exit(0)
	stack = []
	for i in html_list:
		try:
			html = i['{}-caption'.format(type)]
			try:
				href = BeautifulSoup(html,'lxml').findAll('a')[0].get('href')
			except IndexError as e:
				continue
				print('[@] IndexError {}'.format(e))
			othersite = urlparse(href).netloc.split('.')[0]
			stack.append(othersite)
			print("[&] Source from User:{}".format(othersite))
		except KeyError as e:
			print('[@] KeyError: {}'.format(e))
			continue

	return stack
	
	
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
	start = 0
	chunk = 20
	with open('test.txt','wb') as f:
		while True:
		# 	t = tumblr('',chunk,'photo',start)
		# 	start += chunk
			t = tumblr('',chunk,'photo',start)
			f.write("\n".join(t))
			start += chunk
