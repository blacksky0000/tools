import get_url as g
import download_file as d
from threading import Thread
import time
import requests as r

	
def	auto(site, type, start=0, chunk=20):
	data = g.tumblr(site, chunk, type, start)
	if not data:
		return
	for j,i in enumerate(data):
		print('Start at {}'.format(j+start))
		print('[URL]: {}'.format(i))
		d.download_with_url(i)
		time.sleep(1)
		print('Finish download.')
		
		
def check_exists(file_name):
	f1 = open('test1.txt','wb');
	with open(file_name,'r') as f:
		for i, line in enumerate(f):
			user_name = line.rstrip('\n')
			res = r.get('http://{}.tumblr.com/api/read?num={}&type={}&start={}'.format(user_name, 1, 'photo', 0))
			if res.status_code != r.codes.ok:
				print("[@] num: {} Request_code: {}, User: {} not found.".format(i, res.status_code, user_name))
				continue
			else:
				f1.write('user: {}\n'.format(user_name))
				print("[+] num: {} User: {} exists".format(i, user_name))


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
	# auto('','video',10, 10)
	# check_exists('test.txt.tmp')
	uniq('test1.txt')
