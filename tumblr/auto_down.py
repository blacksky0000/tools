import get_url as g
import download_file as d
from threading import Thread
import time

	
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
		
		
auto('','video',10, 10)

