import requests as r
import xmltodict, re
import threading
import json,sys
from bs4 import BeautifulSoup
from urlparse import urlparse

def tumblr(site, chunk, type, start, function=1):
	res = r.get('http://{}.tumblr.com/api/read?num={}&type={}&start={}'.format(site, chunk, type, start))
	if res.status_code != r.codes.ok:
		print("[@] Request_code: {}, User not found.".format(res.status_code))
		sys.exit(1)

	dicts = xmltodict.parse(res.content)

	print "[+] Total: {}".format(dicts['tumblr']['posts']['@total'])
	# return res

	if function == 1:
		return get_redirect(dicts, type)
	if function == 2:
		return get_source(dicts, type, start, chunk)

def get_redirect(data, type):
	try:
		html_list = data['tumblr']['posts']['post']
	except KeyError as e:
		print('[@] KeyError: {}'.format(e))
		return None

	stack = []
	for i in html_list:
		try:
			html = i['{}-caption'.format(type)]
			try:
				href = BeautifulSoup(html, "html.parser").findAll('a')[0].get('href')
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
	posts = []
	stack = []
	try:
		posts = data['tumblr']['posts']['post']
		print "find {} elements".format(len(posts))

	except KeyError as e:
		print(e)
		return None
	
	try:
		if type == 'photo':

			for i, post in enumerate(posts):
				try:

					if post['photo-url']:
						stack.append(post['photo-url'][0]['#text'])

					if post['photoset']:
						for j, sub_post in enumerate(post['photoset']['photo']):
							# print post['photoset']['photo'][j]['photo-url'][0]['#text']
							# print 
							stack.append(post['photoset']['photo'][j]['photo-url'][0]['#text'])
					else:
						continue

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
	print tumblr('',1,'photo',6, 2).content
	