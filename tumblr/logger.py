
import logging
import logging.handlers
import sys


def set_logger(file_name):
	DEBUG = logging.INFO
	if len(sys.argv) > 1 and sys.argv[1] == 'debug':
		DEBUG = logging.NOTSET

	print DEBUG

	logger = logging.getLogger(__name__)
	logger.setLevel(DEBUG)

	handler = logging.handlers.RotatingFileHandler(file_name, maxBytes = 10 ** 4)

	logger.addHandler(handler)

	return logger




if __name__ == '__main__':
	logger = set_logger('tumblr.log')

	for i in range(3):
		logger.info('info {}'.format(i))
		logger.debug('debug {}'.format(i))
		logger.warning('warning {}'.format(i))