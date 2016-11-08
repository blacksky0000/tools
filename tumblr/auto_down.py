import get_url as g
import download_file as d
from threading import Thread
import queue,time

	
def	auto(site, type, start=0, chunk=20):
	data = g.tumblr(site, chunk, type, start)
	if not data:
		return
	for i in data:
		print('[URL]: {}'.format(i))
		d.download_with_url(i)
		time.sleep(1)
		
		
threads =[]	
s = 0
for i in range(3):
	t = Thread(target=auto, args=('mobpsycho100','photo',s, 20,))
	threads.append(t)
	t.start()
	s += 20
s = 0
for i in range(3):
	t = Thread(target=auto, args=('mobpsycho100','video',s, 20,))
	threads.append(t)
	t.start()
	s += 20
		
for t in threads:
	t.join()
