## Script to save request to Uber Suge API ##

import requests
import json
import MySQLdb

# Initiate cursor
cnx = MySQLdb.connect(host='', port=3306, passwd='gamera@1234', user='gsmp', db='gsmp')
cursor = cnx.cursor()

start_long, start_lat = '42.340152', '-71.089389'
end_long, end_lat = '42.318911', '-71.113336'

# Formate URL with auth key and locations
headers = { 'Authorization': 'Token 1tmfoN1a7nquX5cIV96_ur_1RioQrHqxuxWcKDNi' }
base_url = 'https://api.uber.com/v1/estimates/price?start_latitude=%s&start_longitude=%s&end_latitude=%s&end_longitude=%s'
url = base_url % (start_long, start_lat, end_long, end_lat)

# Make request
r = requests.get(url, headers=headers)
#print r.text

# Parse JSON
decoded = json.loads(r.text)
black = decoded['prices'][0]['surge_multiplier']
suv = decoded['prices'][1]['surge_multiplier']
taxi = decoded['prices'][2]['surge_multiplier']
uberX = decoded['prices'][3]['surge_multiplier']
uberXL = decoded['prices'][4]['surge_multiplier']
print black
print suv 
print taxi
print uberX
print uberXL

insert = '''
INSERT INTO `bets`.`Surge`
(
`UberX`,
`UberXL`,
`UberSUV`,
`UberTaxi`)
VALUES
(
%s,
%s,
%s,
%s);
'''

#print r.text
