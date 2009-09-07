#!/usr/bin/python
#
# Copyright (c) 2009 Emanuel Borsboom.  See COPYING.txt for license.
#
# Calculates current atlas chart numbers for the time period of the input.
# Expects CSV output from xtide for the "Point Atkinson, British Columbia"
# location on standard input.
#
# Produces CSV output of this format on standard output, where 'N' is
# the chart number for the date/time:
#
#    YYYY-MM-DD,HH:MM,N
#
# The script corrects for changes to/from daylight saving time (PDT).
#
# Note that this script is only tested on a system that is set to the Pacific
# time zone.  If your system is configured with a different time zone,
# the results may be unpredictable.
#
# Arguments:
#
#    --time-interval <minutes>
#        Specifies the time interval between outputs in minutes.
#        Default is 60 (one hour).
#
# Usage example:
#
#     tide -l "Point Atkinson, British Columbia" -f c -b '2009-02-28 12:00' 
#         -e '2009-04-01 23:59' | ./calculate.py --time-interval 30
#

import sys
import string
import time
import math
import getopt

flood_30_pages = [1,2,3,4,5,6,7,8]
flood_18_pages = [9,10,11,12,13,14,15]
flood_06_pages = [16,17,18,19,20,21]
ebb_30_pages = [22,23,24,25,26,27,28,29]
ebb_18_pages = [30,31,32,33,34,35,36]
ebb_12_pages = [37,38,39,40,41,42,43]

output_time_increment = 60 * 60 # 1 hour

optlist, args = getopt.getopt(sys.argv[1:], '', ['time-interval='])
for o,a in optlist:
	if o == '--time-interval':
		output_time_increment = int(a) * 60

prevht = None
prevtm = None

line = sys.stdin.readline()
while line:
	line = line[0:-1]
	parts = string.split(line,',')
	heightstr=parts[3]
	if len(heightstr)>0:
		datestr = parts[1]
		timestr = parts[2]
		curtm = time.mktime(time.strptime(datestr + ' ' + timestr, "%Y-%m-%d %I:%M %p %Z"))
		curht = float(heightstr[0:-2])
		if prevtm:
			htdiff = (curht - prevht)	
			if htdiff >= 2.4:
				pages = flood_30_pages
			elif htdiff >= 1.2:
				pages = flood_18_pages
			elif htdiff >= 0.0:
				pages = flood_06_pages
			elif htdiff <= -2.4:
				pages = ebb_30_pages
			elif htdiff <= -1.5:
				pages = ebb_18_pages
			else:
				pages = ebb_12_pages
			outtm = ((int(prevtm) + (output_time_increment - 1)) / output_time_increment) * output_time_increment
			while outtm < curtm:
				prevdiff = (outtm - prevtm) / 3600.0
				curdiff = (curtm - outtm) / 3600.0
				if prevdiff < curdiff:
					page = pages[int(round(prevdiff))]
				else:
					page = pages[len(pages) - 1 - int(round(curdiff))]
				print time.strftime("%Y-%m-%d,%H:%M", time.localtime(outtm)) + ',' + str(page)
				outtm += output_time_increment
		prevtm = curtm
		prevht = curht
	#sys.stderr.write('# ' + line + '\n')
	line = sys.stdin.readline()