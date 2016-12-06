from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import download_file as d

def screen_shot(search_name, file_path):
	URL = 'https://{}.tumblr.com/archive'.format(search_name)

	print "[+] Start screenshot for: {}".format(search_name)
	driver = webdriver.PhantomJS()
	driver.set_window_size(1024, 768) # set the window size that you need
	driver.get(URL)
	try:
		element = WebDriverWait(driver, 20).until(EC.visibility_of_any_elements_located((By.CLASS_NAME, 'hover')))
	except TimeoutException as e:
		print "[!] Time out. for user:{}".format(search_name)
		return None
	driver.get_screenshot_as_file('{}/{}.png'.format(save_path, search_name))
	driver.quit()
	print "[-] Save file in: {}/{}".format(file_path, search_name)
	return 'OK'

if __name__ == '__main__':

	file_name = ''
	save_path = './.screen/{}'.format(file_name)

	d.make_dir(save_path)

	with open('./.list/{}.txt'.format(file_name), 'r') as f:
		for line in f:
			time = 0
			while screen_shot(line.rstrip(), save_path) == None:
				time += 1
				if time > 3:
					break
				print '[r] Retry user:{} at {} times.'.format(line.rstrip(), time)
				