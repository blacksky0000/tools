#!/usr/bin/python
import math
import time, sys, re, getopt
import calendar
import pprint

def calc(file):
	with open(file, 'r') as f:
		result = {}
		p = re.compile('\d+')
		p_date = re.compile('\d+/\d+')
		p_time = re.compile("(\d+:\d+\s*-\s*\d+:\d+(\s*\^\s*\d+(\.\d+){0,1}){0,1})")
		for line in f:
			if 'year:' in line:
				d = re.split('\W+', line)
				year = d[1]
				print("year: {}".format(year))
				if not result.has_key(year):
					result[year] = {}

			if 'mon:' in line:
				work_time = earn = .0
				train = 0
				days = 0
				mon= day= start_h= start_m= end_h= end_m = ""
				train_cost = 500 * 2
				cost = 1100 / 60.

				d = re.split('\W+', line)

				month = list(calendar.month_abbr).index(d[1])
				# month = d[1]

				print( 'Mon: {}'.format(month))
				if 'pay' in d:
					cost = float(d[d.index('pay') + 1]) / 60.
					print( 'Cost: {} en.'.format(cost * 60))
				if 'trans' in d:
					train_cost = float(d[d.index('trans') + 1]) * 2
					print( 'trans: {}'.format(train_cost))

			if p_date.match(line):
				data = p.findall(line)
				mon, day = data[0], data[1]

				days += 1
				if 'remote' not in line:
					print('{}/{}:'.format(mon, day))
					train += 1
				else:
					print('{}/{}: <remote>'.format(mon, day))

				times = p_time.findall(line)
				for t in range(len(times)):
					form_date = p.findall(times[t][0])
					rest_h = rest_m = "0"
					if len(form_date) == 4:
						start_h, start_m, end_h, end_m = form_date
					elif len(form_date) == 6:
						start_h, start_m, end_h, end_m, rest_h, rest_m = form_date
					else:
						start_h, start_m, end_h, end_m, rest_h = form_date

					tmp = (float(end_h) - float(start_h) - float(rest_h)) * 60 + (float(end_m) - float(start_m) - float(rest_m))

					work_time += tmp
					earn += math.floor(tmp * cost)
					print( ' work {}:{} -> {}:{}, rest: {}.{} = {} min and earn {:,.2f} en.'.format(start_h, start_m, end_h, end_m, rest_h, rest_m, tmp, tmp * cost))


			if 'pre:' in line:
				pre = int(line.split(':')[1])
				earn -= pre
				print( 'Advance: {:,.2f} and remain: {:,.2f}'.format(pre, earn))
			if 'add:' in line:
				pre = int(line.split(':')[1])
				earn += pre
				print( 'Extra: {:,.2f} and total: {:,.2f}'.format(pre, earn))
			if 'fin' in line:
				if result[year].has_key(month):
					result[year][month] += earn + train * train_cost
				else:
					result[year][month] = earn + train * train_cost
				print( 'At mon: {}, work {} days'.format(mon, days))
				print( 'work: {}:{} -- payment:{:,.2f} + transfer: {:,} = earn: {:,.2f}.\n\n'.format(int(work_time/60), int(work_time%60),earn, train*train_cost, earn + train * train_cost)	)

		pprint.pprint(result, depth=2)

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hr:t")
	except getopt.GetoptError:
		print( 'payment.py -h')
		sys.exit(0)

	for opt, arg in opts:
		if opt == '-h':
			print( 'payment.py -r <file>\tRun calc')
			print( 'payment.py -t\tTemplate of file')
		elif opt == '-r':
			calc(arg)
		elif opt == '-t':
			print( 'Template:')
			print( '\tmon: <Month>, cost: <Cost=1000>, trans: <trans=500/one_way>')
			print( '\t<mon>/<day> <start_hour>:<start_min> - <end_hour>:<end_min>')
			print( '\tpre: <price>')
			print( '\tadd: <count>')
			print( '\tfin')
			print
			print( 'Time is 24h format.')

	if not opts:
		print( 'payment.py -h')
		sys.exit(0)




if __name__ == '__main__':
	main()
