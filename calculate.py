#!/usr/bin/python
#
# Copyright (c) 2009 Emanuel Borsboom.  See COPYING.txt for license.
#
# Calculates current atlas chart numbers for the time period of the input.
# Expects CSV output from xtide for the "Point Atkinson, British Columbia"
# location on standard input.
#
# Produces CSV output of this format on standard output, where 'N' is
# the chart number for the date/time, and D is the deviation in minutes
# of the chart's time from the output time:
#
#    YYYY-MM-DD,HH:MM,N,D
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

flood_30_info = { 'pages' : [1,2,3,4,5,6,7,8],
                  'cycles': 1.0259 }
flood_18_info = { 'pages' : [9,10,11,12,13,14,15],
				  'cycles': 1.0516 }
flood_06_info = { 'pages' : [16,17,18,19,20,21],
				  'cycles': 1.0558 }
ebb_30_info   = { 'pages' : [22,23,24,25,26,27,28,29],
				  'cycles': 1.0576 }
ebb_18_info   = { 'pages' : [30,31,32,33,34,35,36]												,
				  'cycles': 1.0174 }
ebb_12_info   = { 'pages' : [37,38,39,40,41,42,43]																,
				  'cycles': 1.1756 }

output_time_increment = 60 * 60 # 1 hour

def calc_pagetmdev(pagepos,cycles,pages,curtm,prevtm,pagebias):
	return (round(pagepos) - (pagepos-pagebias)) * cycles / (len(pages)-1) * (curtm - prevtm)

optlist, args = getopt.getopt(sys.argv[1:], '', ['time-interval='])
for o,a in optlist:
	if o == '--time-interval':
		output_time_increment = int(a) * 60

prevht = None
prevtm = None
offset_next_outtm = 0
prevpage = None

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
				info = flood_30_info
			elif htdiff >= 1.2:
				info = flood_18_info
			elif htdiff >= 0.0:
				info = flood_06_info
			elif htdiff <= -2.4:
				info = ebb_30_info
			elif htdiff <= -1.5:
				info = ebb_18_info
			else:
				info = ebb_12_info
			pages = info['pages']
			cycles = info['cycles']
			outtm = ((int(prevtm) + (output_time_increment - 1)) / output_time_increment) * output_time_increment + offset_next_outtm
			offset_next_outtm = 0
			while outtm < curtm:
				cyclepos = (outtm - prevtm) / (curtm - prevtm)
				pagepos = cyclepos * (len(pages)-1) / cycles
				page = pages[int(round(pagepos))]
				pagetmdev = calc_pagetmdev(pagepos,cycles,pages,curtm,prevtm,0.0)
				if pagetmdev > curtm - outtm:
					# The next cycle actually starts closer to the current time
					# than the nearest point on the current cycle, so skip to next
					# cycle.
					offset_next_outtm = -output_time_increment
					break				
				if page == prevpage:
					# If we have a page repeat, bias slightly toward the
					# next page, but make sure we don't repeat the bias
					# next time
					prevpage = page
					pagepos += 0.1
					page = pages[int(round(pagepos))]
					pagetmdev = calc_pagetmdev(pagepos,cycles,pages,curtm,prevtm,0.1)
				else:
					prevpage = page
				print (time.strftime("%Y-%m-%d,%H:%M", time.localtime(outtm)) + 
				       ',' + 
				       str(page) + 
				       ',' + 
				       '%+f' % (pagetmdev / 60))
				outtm += output_time_increment
		prevtm = curtm
		prevht = curht
	#sys.stderr.write('# ' + line + '\n')
	line = sys.stdin.readline()