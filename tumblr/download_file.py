import requests as r;
import re, urllib, os, sys
from name_gen import getName
import hashlib
from tqdm import tqdm
from urlparse import urlparse

CHUNK_SIZE = 2048

def download_with_url(url, file_path='./'):
	try:
		res = r.get(url, stream=True);
	except:
		return

	file_len = res.headers.get('Content-Length')
	file_type = res.headers.get('Content-type')

	if file_len is None or file_type is None:
		print('[?] Length or Type missing')
		return

	parse = urlparse(url)
	full_path = file_path + parse.netloc

	buf = ""
	hash = hashlib.md5()

	pbar = tqdm(total=int(file_len), unit="B", unit_scale=True)
	for chunk in res.iter_content(2048):
		buf += chunk
		hash.update(chunk)
		pbar.update(len(chunk))

	pbar.close()

	file_name = hash.hexdigest()
	print('[+] File hash is:{}'.format(file_name))

	make_dir(full_path)
	return save_file(buf, '{}/{}'.format(full_path,'{}.{}'.format(file_name,file_type.split('/')[-1])))


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
		# for chunk in buf:
		# 	f.write(chunk)
		f.write(contents)

		print('[+] created new file:{}'.format(path.split('/')[-1]))


if __name__ == '__main__':
	download_with_url("http://download.thinkbroadband.com/100MB.zip")

