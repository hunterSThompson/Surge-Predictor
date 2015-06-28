#!/usr/bin/env python

import requests
import json
import MySQLdb
import sklearn as sk
import numpy
import pygal

qryStr = 'SELECT DATE_SUB(Time, INTERVAL 4 HOUR), UberX FROM Surge WHERE DATE(DATE_SUB(Time, INTERVAL 4 HOUR)) = DATE(NOW()) AND location = \'Home\''

q2 = 'SELECT DAY(DATE_SUB(Time, INTERVAL 4 HOUR)), HOUR(DATE_SUB(Time, INTERVAL 4 HOUR)), UberX, UberBlack FROM Surge WHERE DATE(DATE_SUB(Time, INTERVAL 4 HOUR)) = DATE(DATE_SUB(NOW(), INTERVAL 28 HOUR)) AND Location= \'Faneuil\''

q3 = 'SELECT DATE_SUB(Time, INTERVAL 4 HOUR), UberX, UberBlack FROM Surge WHERE DATE(DATE_SUB(Time, INTERVAL 4 HOUR)) = DATE(DATE_SUB(NOW(), INTERVAL 52 HOUR)) AND Location= \'Faneuil\''

q4 = 'SELECT DATE_SUB(Time, INTERVAL 4 HOUR), UberX, UberBlack FROM Surge WHERE DATE(DATE_SUB(Time, INTERVAL 4 HOUR)) = DATE(DATE_SUB(NOW(), INTERVAL %s HOUR)) AND Location= \'%s\''


def calcStats(chunk):
	avg = sum(chunk) / len(chunk)
	s = 0
	for i in chunk:
		s += ((avg-i)**2)
	var = s / len(chunk)
	return avg, var
	
def createBins(lst, n):
	bins = []
	for i in range(0, len(lst), n):
		chunk = lst[i:i+n]
		bins.append(calcStats(chunk))
		#bins.append(lst[i:i+n])
	return bins

def createChart(x, y):
	#import pdb; pdb.set_trace()
	chart = pygal.Line()
	chart.title = 'Some shit'
	chart.x_labels = x
	chart.add('Faneuil', y)
	chart.render_in_browser()
	chart.render_to_file('Faneuil.html')

try:
	cnx = MySQLdb.connect(host='54.88.34.236', port=3306, passwd='gamera@1234', user='bets', db='bets')
	cursor = cnx.cursor()
	cursor.execute(q3)
	f = open('output2.csv', 'w')
	accum = ''
	surges = []
	times = []

	for time, x, black in cursor.fetchall():
		#dset.append((time, black))
		surges.append(black)
		times.append(str(mins))

		mins = (time.hour * 60) + time.minute
		vals = (mins, x, black)
		vals2 = (str(time), x, black)
		values = ','.join(map(str, vals))
		values2 = ','.join(map(str, vals2))
		accum += (values + '\n')
	#bins = createBins(dset, 15)
	#import pdb; pdb.set_trace()
	createChart(times, surges)
	f.write(accum)

except Exception, e:
	print e
#except Exception as e:
    #exc_type, exc_obj, exc_tb = sys.exc_info()
    #fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #print(exc_type, fname, exc_tb.tb_lineno)
