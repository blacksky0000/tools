#!/Users/kingno21/.virtualenvs/test/bin/python
import get_url as g
import download_file as d
from threading import Thread
import time
import requests as r
import sort_uniq as s


def	auto(site, type, start=0, chunk=20, function=2):
	data = g.tumblr(site, chunk, type, start, function)

	if data == None:
		return None
	if not data:
		return []
	if function == 1:
		name_list = list(set(data))
		return check_exists(name_list)
	elif function == 2:
		for j,i in enumerate(data):
			print('[Chunck]: {}'.format(j+1))
			print('[URL]: {}'.format(i))
			d.download_with_url(i)
			time.sleep(1)
			print('Finish download.')

def check_exists(data, file_name=None):
	if data is None:
		f1 = open('test1.txt','ab+');
		with open(file_name,'r') as f:
			for i, line in enumerate(f):
				user_name = line.rstrip('\n')
				try:
					res = r.get('http://{}.tumblr.com/'.format(user_name))
				except r.exceptions.InvalidURL as e:
					print("[@] Error: {}, InvalidURL".format(e))
					continue

				if res.status_code != r.codes.ok:
					print("[@] num: {} Request_code: {}, User: {} not found.".format(i, res.status_code, user_name))
					continue
				else:
					f1.write('user: {}\n'.format(user_name))
					print("[+] num: {} User: {} exists".format(i, user_name))

	else:
		exists = []
		for i, line in enumerate(data):
			user_name = line.rstrip('\n')
			try:
				res = r.get('http://{}.tumblr.com/'.format(user_name))
			except r.exceptions.InvalidURL as e:
				print("[@] Error: {}, InvalidURL".format(e))
				continue

			if res.status_code != r.codes.ok:
				print("[@] num: {} Request_code: {}, User: {} not found.".format(i, res.status_code, user_name))
				continue

			else:
				exists.append(user_name)
				print("[+] num: {} User: {} exists".format(i, user_name))

		return exists


if __name__ == '__main__':


	tmp_file = 'list.txt'
	search_name = ''
	search_type = 'photo'
	save_path = '.list'
	start = 0
	chunk = 20
	spy_or_down = 1


	with open(tmp_file, "ab+") as f:
		while True:
			print("[!] Start with {}".format(start))
			tmp = auto(search_name, search_type, start, chunk, spy_or_down)
			if tmp == None:
				break
			try:
				for line in list(set(tmp)):
					f.write("{}\n".format(line))
			except TypeError as e:
				print(e)

			start += chunk

	s.sort_uniq(tmp_file, search_name, search_type, save_path)


















