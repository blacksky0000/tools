import get_url as g
import download_file as d
from threading import Thread
import time
import requests as r


def	auto(site, type, start=0, chunk=20, function=2):
	data = g.tumblr(site, chunk, type, start, function)
	if not data:
		return
	if function == 1:
		name_list = list(set(data))
		return check_exists(name_list)
	elif function == 2:
		for j,i in enumerate(data):
			print('Start at {}'.format(j+start))
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



def uniq(file_name):
	stack = []
	with open(file_name, 'r') as f:
		for line in f:
			stack.append(line.rstrip('\n'))
		f.close()

	with open(file_name, 'wb') as f:
		for i, line in enumerate(list(set(stack))):
			f.write("{}\n".format(line))
			print("[+] num: {:03} User: {}".format(i, line))


if __name__ == '__main__':
	start = 524
	chunk = 20
	with open("list.txt", "ab+") as f:
		while True:
			print("[!] Start with {}".format(start))
			tmp = auto('','photo', start, chunk, 2)
			try:
				for line in list(set(tmp)):
					f.write("{}\n".format(line))
			except TypeError as e:
				print(e)

			start += chunk

















