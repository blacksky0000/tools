import requests as r;
import re, urllib, os, sys
from name_gen import getName
import hashlib
from tqdm import tqdm
from urlparse import urlparse

CHUNK_SIZE = 2048

def download_with_url(url, file_path='./'):
	res = r.get(url, stream=True);

	file_len = res.headers.get('Content-Length')
	file_type = res.headers.get('Content-type')

	if file_len is None or file_type is None:
		print('[?] Length or Type missing')
		return

	parse = urlparse(url)
	full_path = file_path + parse.netloc

	hash = hashlib.md5()
	hash.update(res.content)
	file_name = hash.hexdigest()
	print('[+] File hash is:{}'.format(file_name))

	make_dir(full_path)
	return save_file(res.iter_content(CHUNK_SIZE), '{}/{}'.format(full_path,'{}.{}'.format(file_name,file_type.split('/')[-1])), int(file_len))


def make_dir(path):
	if not os.path.exists(path):
		os.makedirs(path)
		print('[+] {} is created'.format(path))
	else:
		print('[*] {} is exists'.format(path))


def save_file(contents, path, size):
	if os.path.isfile(path):
		print('[!] file exist')
		return True
	pbar = tqdm(total=size, unit='B', unit_scale=True)
	with open(path, 'wb') as f:
		for chunk in tqdm(contents):
			f.write(chunk)
			pbar.update(len(chunk))
		pbar.close()
		print('[+] created new file:{}'.format(path.split('/')[-1]))




