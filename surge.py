#!/usr/bin/env python

## Script to save request to Uber Suge API ##

import requests
import json
import MySQLdb

start_long, start_lat = '42.340152', '-71.089389'
end_long, end_lat = '42.318911', '-71.113336'

# Read in what locations to log surge for from locations.txt
locations = [ ]
for line in open('locations.txt', 'r'):
	locations.append(tuple(line.split(',')))
print 'Locations:\n' + str(locations)

# Formate URL with auth key
headers = { 'Authorization': 'Token 1tmfoN1a7nquX5cIV96_ur_1RioQrHqxuxWcKDNi' }
base_url = 'https://api.uber.com/v1/estimates/price?start_latitude=%s&start_longitude=%s&end_latitude=%s&end_longitude=%s'



for (loc, lon, lat) in locations:

	#import pdb; pdb.set_trace()
	try:

		# Formate URL to enclude start lat/long
		url = base_url % (lon, lat, end_long, end_lat)

		# Make request
		r = requests.get(url, headers=headers)

		# Parse JSON
		decoded = json.loads(r.text)
		black = decoded['prices'][0]['surge_multiplier']
		suv = decoded['prices'][1]['surge_multiplier']
		taxi = decoded['prices'][2]['surge_multiplier']
		uberX = decoded['prices'][3]['surge_multiplier']
		uberXL = decoded['prices'][4]['surge_multiplier']
		print '\n' + loc
		print black
		print suv 
		print taxi
		print uberX
		print uberXL

		# Insert into DB
		#data = (black, uberX, uberXL, suv, taxi, start_long, start_lat)
		data = (black, uberX, uberXL, suv, taxi, lon, lat, loc)
		insert = '''
		INSERT INTO `bets`.`Surge`
		(
		`Time`,
		`UberBlack`,
		`UberX`,
		`UberXL`,
		`UberSUV`,
		`UberTaxi`,
		`Longitude`,
		`Latitude`,
		`Location`
		)
		VALUES
		(
		NOW(),
		%s,
		%s,
		%s,
		%s,
		%s,
		%s,
		%s,
		%s);
		'''
		
		#print insert % data
		#pass
	
		# Initiate cursor
		cnx = MySQLdb.connect(host='', port=3306, passwd='gamera@1234', user='bets', db='bets')
		cursor = cnx.cursor()
		cursor.execute(insert, data)
		cnx.commit()
	except Exception, e:
		open('error.txt', 'a').write('error: ' + loc + '\n')
