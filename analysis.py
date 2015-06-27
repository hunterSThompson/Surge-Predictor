#!/usr/bin/env python

import requests
import json
import MySQLdb

qryStr = 'SELECT DATE_SUB(Time, INTERVAL 4 HOUR), UberX FROM Surge WHERE DATE(DATE_SUB(Time, INTERVAL 4 HOUR)) = DATE(NOW()) AND location = \'Home\''
q2 = 'SELECT DAY(DATE_SUB(Time, INTERVAL 4 HOUR)), HOUR(DATE_SUB(Time, INTERVAL 4 HOUR)), UberX, UberBlack FROM Surge WHERE DATE(DATE_SUB(Time, INTERVAL 4 HOUR)) = DATE(DATE_SUB(NOW(), INTERVAL 28 HOUR)) AND Location= \'Faneuil\''
q3 = 'SELECT DATE_SUB(Time, INTERVAL 4 HOUR), UberX, UberBlack FROM Surge WHERE DATE(DATE_SUB(Time, INTERVAL 4 HOUR)) = DATE(DATE_SUB(NOW(), INTERVAL 28 HOUR)) AND Location= \'Faneuil\''

try:
	cnx = MySQLdb.connect(host='', port=3306, passwd='gamera@1234', user='bets', db='bets')
	cursor = cnx.cursor()
	cursor.execute(q3)
	f = open('output.csv', 'w')
	accum = ''
	#for data in cursor.fetchall():
	for time, x, black in cursor.fetchall():
		print time.hour
		print time.minute
		mins = (time.hour * 60) + time.minute
		print mins
		vals = (mins, x, black)
		vals2 = (str(time), x, black)
		values = ','.join(map(str, vals))
		values2 = ','.join(map(str, vals2))
		#accum += (values + '\n')
		accum += (values2 + '\n')
	f.write(accum)
except Exception, e:
	#open('error.txt', 'a').write('error: ' + loc + '\n')
	print e
