import os

def sort_uniq(tmp_file, search_name, search_type, save_path='.'):

	f = open(tmp_file, 'rb')
	lines = set(sorted([ line for line in f ]))

	with open("{}/{}_{}.txt".format(save_path, search_name, search_type), 'wb') as f:
		for line in lines:
			f.write(line)

	os.remove(tmp_file)


if __name__ == '__main__':
	sort_uniq('list.txt', '', 'photo')