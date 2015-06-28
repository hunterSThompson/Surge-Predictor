## Code to run existing model for a specifc date/location ##

import sys
import math
import os
import re
from datetime import datetime
import time

if len(sys.argv) < 2:
	sys.exit("No target date/time supplied!")
target_date = time.strptime(sys.argv[1], "%Y-%m-%d %H:%M:%S")

loc = len(sys.argv) > 2 # any 3rd arg means location is in cambridge

bins = [file for file in os.listdir('BinData') if file.endswith('.bin')]

# Make decision on 'trend area' (Boston vs Cambridge in our case)
# If (Cambridge only average Cambridge, if boston average boston surges.)
if loc:
	bins = filter(lambda x: 'MIT' in x, bins)
else:
	bins = filter(lambda x: 'MIT' not in x, bins)

def checkdate(s):
	date = s[s.index('_')+1 : s.index('.')]
	tstruct = time.strptime(date, '%Y-%m-%d') # parse time
	return target_date.tm_wday == tstruct.tm_wday

# Make decision on weekday vs. Thurs/fri/sat/sunday
bins = filter(lambda x: checkdate(x), bins)

# Calculate min number to figure out what bin to look in
bin_num = int(math.floor((target_date.tm_hour * 60 + target_date.tm_min)/15))
print bin_num

# Parse each bin file and grab the value we need
pairs = []
for b in bins:
	data = open('BinData/' + b).readlines()
	avg, var = tuple(data[bin_num].split(','))
	var = float(var.replace('\n', ''))
	avg = float(avg)
	pairs.append((avg, var))

# Now take 
sx, sv = 0.0, 0.0
for x, v in pairs:
	sx = sx + x
	sv = sv + v

ax = sx / len(pairs)
av = sv / len(pairs)

print 'Predicted surge: %s' % ax
print 'with a variance of +/- %s' % av
