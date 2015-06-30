#!/usr/bin/env python

import requests
import json
import MySQLdb
import sklearn as sk
import numpy
import pygal
import sys
import os
from datetime import date, timedelta

day = 1
if len(sys.argv) > 1:
	day = int(sys.argv[1])

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
	return bins

def calcDate(offset):
	return date.today() - timedelta(days=offset)
	

def createChart(_d, t, x, y):
	chart = pygal.Line()

	title = t + '_' + str(_d)
	chart.title = title

	chart.x_labels = x
	chart.add(title, y)
	chart.render_in_browser()
	chart.render_to_file('Charts/' + title + '.html')

def writeBin(_loc, date_read, b):
	filename = 'BinData/' + _loc +'_' + str(date_read) + '.bin'
	str_data = '\n'.join(map(lambda t: ', '.join(str(i) for i in t), b))
	open(filename, 'w').write(str_data)

# Read in locations from locations.txt
locations = []
for line in open('locations.txt', 'r'):
        locations.append(tuple(line.split(',')))
print 'Locations:\n' + str(locations)

# Create a graph and .bin file each location
for loc, lat, lon in locations:
	try:
		# Query surges for this location/date range
		cnx = MySQLdb.connect(host='54.88.34.236', port=3306, passwd='gamera@1234', user='bets', db='bets')
		cursor = cnx.cursor()
		qstr = q4 % ((day*24)+4, loc)
		cursor.execute(qstr)

		surges,	times, dset = [], [], []
		for time, x, black in cursor.fetchall():
			dset.append(black)
			mins = (time.hour * 60) + time.minute
			surges.append(black)
			times.append(str(mins))
	
		#import pdb; pdb.set_trace()
		reading_date = calcDate(day)

		bins = createBins(dset, 15)
		writeBin(loc, reading_date, bins)

		createChart(reading_date, loc, times, surges)
	#except Exception, e:
		#print e
	except Exception as e:
    		exc_type, exc_obj, exc_tb = sys.exc_info()
    		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    		print(exc_type, fname, exc_tb.tb_lineno, e)
