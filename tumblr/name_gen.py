import random

AL = 'QAZWSXEDCRFVTGBYHNUJMIKOPLqazwsxedcrfvtgbyhnujmikolp1234567890'

def getName():
	name = ''
	for i in range(32):
		name += AL[random.randint(0, len(AL)-1)]
	return name	

