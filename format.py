#!/usr/bin/python
#
# Copyright (c) 2009 Emanuel Borsboom.  See COPYING.txt for license.
#
# Formats the output of calculate.py to a table in text or HTML format.
#
# The output from calculate.py may NOT use a time interval that exceeds 60,
# and must evenly divide 60 (so 60, 30, and 15 would be acceptable).
#
# This will only display dates for which a full day's data is available.
# That means the xtide output that calculate.py is run from needs to
# include at least the full tide before and after the desired date range.
# An easy way to do this is to have xtide start 12 hours before and 12 hours
# after the date range.
#
# Arguments:
#
#   --html
#       Format the output in HTML.  Otherwise, text is produced.
#
#   --date-format "<format>"
#       Specifies the date format, using a format string as specified
#       in the documentation for python's time.strftime() function:
#           http://www.python.org/doc/2.5.1/lib/module-time.html
#       Default is "%a %d %b, %Y".
#
#    --time-format "<format>"
#       Specifies the date format, using a format string as specified
#       in the documentation for python's time.strftime() function:
#           http://www.python.org/doc/2.5.1/lib/module-time.html
#       Default is "%H%M".
#
#    --columns <n>
#        Specifies the maximum number of columns in the output table.
#        If the amount of data points for a day exceeds this, 
#        extras are put on a new row.
#        Default is 24.
#
# Usage Example:
#
#   tide -l "Point Atkinson, British Columbia" -f c -b '2009-02-28 12:00' 
#       -e '2009-04-01 23:59' | ./calculate.py --time-interval 30 | 
#       ./format.py  --date-format "%a %d" --time-format '%H:%M' --columns 12
#

import sys
import string
import time
import getopt

html = False
max_cols_per_row = 24
date_format = '%a %d %b, %Y'
time_format = '%H%M'

optlist, args = getopt.getopt(sys.argv[1:], '', ['html','date-format=','time-format=','columns='])
for o,a in optlist:
	if o == '--html':
		html = True
	elif o == '--date-format':
		date_format = a
	elif o == '--time-format':
		time_format = a
	elif o == '--columns':
		max_cols_per_row = int(a)
		
found_first_day = False
got_headers = False
headers = []
time_indices = {}
values = []

oddeven = "odd"

line = sys.stdin.readline()
while line:
	if len(line) > 0 and line[0] != '#':
		line = line[0:-1]
		parts = string.split(line,',')
		timestr = parts[1]
		if found_first_day or timestr == '00:00':
			datestr = parts[0]
			page = parts[2]
			if found_first_day and timestr == '00:00':
				prevdatefmt = time.strftime(date_format, time.strptime(prevdatestr, '%Y-%m-%d'))
				if not got_headers:
					got_headers = True
					if html:
						print '<table class="ca_table"><tr class="ca_tr ca_tr_header1"><td class="ca_td ca_td_headerdate1"></td>'
					else:
						sys.stdout.write(' ' * len(prevdatefmt) + ' | ')
					colidx = 0
					rowidx = 0
					for header in headers:
						if colidx >= max_cols_per_row:
							rowidx += 1
							if html:
								print '</tr><tr class="ca_tr ca_tr_header' + str(rowidx+1) + '"><td class="ca_td ca_td_headerdate' + str(rowidx+1) + '"></td>'
							else:
								sys.stdout.write('\n' + ' ' * len(prevdatefmt) + ' | ')
							colidx = 0
						if html:
							print '<td class="ca_td ca_td_headertime' + str(rowidx+1) + '">' + header + '</td>'
						else:
							sys.stdout.write('%s ' % header)
						colidx += 1
					if html:
						print '</tr>'
					else:
						sys.stdout.write('\n' + '-' * len(prevdatefmt) + '-+')
						colidx = 0
						for header in headers:
							if colidx >= max_cols_per_row:
								break
							sys.stdout.write('-' + ('-' * len(headers[colidx])))
							colidx += 1
						sys.stdout.write('\n')
				if html:
					print '<tr class="ca_tr ca_tr_' + oddeven + '1"><td class="ca_td ca_td_' + oddeven + 'date1">' + prevdatefmt + '</td>'
				else:
					sys.stdout.write('%s |' % prevdatefmt)
				colidx = 0
				rowidx = 0
				for value in values:
					if colidx >= max_cols_per_row:
						rowidx += 1
						if html:
							print '</tr><tr class="ca_tr ca_tr_' + oddeven + str(rowidx+1) + '"><td class="ca_td ca_td_' + oddeven + 'date' + str(rowidx+1) + '"></td>'
						else:
							sys.stdout.write('\n' + ' ' * len(prevdatefmt) + ' |')
						colidx = 0
					if len(value) > 0:
						if html:
							print '<td class="ca_td ca_td_' + oddeven + 'page' + str(rowidx+1) + '">%02d</td>' % int(value)
						else:
							sys.stdout.write((' %02d' % int(value)) + (' ' * (len(headers[colidx]) - 2)))
					else:
						if html:
							print '<td class="ca_td ca_td_' + oddeven + 'page' + str(rowidx+1) + '"></td>'
						else:
							sys.stdout.write(' ' + (' ' * len(headers[colidx])))
					colidx += 1
				if html:
					print '</tr>'
				else:
					sys.stdout.write('\n')
				if oddeven == 'odd': 
					oddeven = 'even'
				else: 
					oddeven = 'odd'
				values = []
			if not got_headers and not time_indices.has_key(timestr):
				headers.append(time.strftime(time_format, time.strptime(timestr, '%H:%M')))
				time_indices[timestr] = len(headers) - 1
			time_index = time_indices[timestr]
			while len(values) <= time_index:
				values.append('')
			values[time_index] = page
			found_first_day = True
			prevdatestr = datestr		
	line = sys.stdin.readline()
	
if html:
	print '</table>'