import requests as r;
import re, urllib, os, sys
from name_gen import getName
import hashlib

CHUNK_SIZE = 2048

def download_with_url(url, file_path='./'):
	res = r.get(url, stream=True);
	try:
		file_len = res.headers['Content-Length']
		file_type = res.headers['Content-type']
	except KeyError as e:
		print('[!] No params provided')
		return False

	parse = urllib.parse.urlparse(url)
	full_path = file_path + parse.netloc

	hash = hashlib.md5()
	hash.update(res.content)
	file_name = hash.hexdigest()
	print('[+] File hash is:{}'.format(file_name))

	make_dir(full_path)
	return save_file(res.iter_content(CHUNK_SIZE), '{}/{}'.format(full_path,'{}.{}'.format(file_name,file_type.split('/')[-1])))


def make_dir(path):
	if not os.path.exists(path):
		os.makedirs(path)
		print('[+] {} is created'.format(path))
	else:
		print('[*] {} is exists'.format(path))


def save_file(contents, path):
	if os.path.isfile(path):
		print('[!] file exist')
		return True
	with open(path, 'wb') as f:
		for chunk in contents:
			f.write(chunk)
		print('[+] created new file:{}'.format(path.split('/')[-1]))




