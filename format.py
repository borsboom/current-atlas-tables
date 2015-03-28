#!/usr/bin/python
#
# Copyright (c) 2009-2011 Emanuel Borsboom.  See COPYING.txt for license.
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
#    --header-time-format "<format>"
#       Specifies the time format used below the pages, using a format string 
#       as specified in the documentation for python's time.strftime() 
#       function:
#           http://www.python.org/doc/2.5.1/lib/module-time.html
#       Default is "%H%M".
#
#    --time-format "<format>"
#       Specifies the time format used in the header, using a format string 
#       as specified in the documentation for python's time.strftime() 
#       function:
#           http://www.python.org/doc/2.5.1/lib/module-time.html
#       Default is "%H%M".
#
#    --columns <n>
#        Specifies the maximum number of columns in the output table.
#        If the amount of data points for a day exceeds this, 
#        extras are put on a new row.
#        Default is 24.
#
#    --deviations
#        If specified, the output includes the actual time that the chart 
#        most closely matches.  Only valid with HTML output.
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
csv = False
show_deviations = False
max_cols_per_row = 24
date_format = '%a %d %b, %Y'
time_format = header_time_format = '%H%M'

optlist, args = getopt.getopt(sys.argv[1:], '', ['html','csv','date-format=','header-time-format=','time-format=','columns=','deviations'])
for o,a in optlist:
	if o == '--html':
		html = True
	elif o == '--csv':
		csv = True
	elif o == '--date-format':
		date_format = a
	elif o == '--header-time-format':
		header_time_format = a
	elif o == '--time-format':
		time_format = a
	elif o == '--columns':
		max_cols_per_row = int(a)
	elif o == '--deviations':
		show_deviations = True
		
found_first_day = False
got_headers = False
headers = []
time_indices = {}
values = []
dst_start_tm = None
dst_end_tm = None
table_start_tm = None

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
			deviation = float(parts[3])
			tm = time.strptime(datestr + ' ' + timestr, '%Y-%m-%d %H:%M')
			if table_start_tm == None:
				table_start_tm = tm
			if found_first_day and timestr == '00:00':
				prevdatefmt = time.strftime(date_format, time.strptime(prevdatestr, '%Y-%m-%d'))
				if not got_headers:
					got_headers = True
					if html:
						print '<table class="ca_table" cellspacing="0" cellpadding="0" border="0"><tr class="ca_tr ca_tr_header1"><td class="ca_td ca_td_headerdate1"></td>'
					elif csv:
						sys.stdout.write('Date')
					else:
						sys.stdout.write(' ' * len(prevdatefmt) + ' | ')
					colidx = 0
					rowidx = 0
					for header in headers:
						if colidx >= max_cols_per_row:
							rowidx += 1
							if html:
								print '</tr><tr class="ca_tr ca_tr_header' + str(rowidx+1) + '"><td class="ca_td ca_td_headerdate' + str(rowidx+1) + '"></td>'
							elif csv:
								print ','
							else:
								sys.stdout.write('\n' + ' ' * len(prevdatefmt) + ' | ')
							colidx = 0
						if html:
							print '<td class="ca_td ca_td_headertime' + str(rowidx+1) + '">' + header + '</td>'
						elif csv:
							sys.stdout.write(',%s' % header)
						else:
							sys.stdout.write('%s ' % header)
						colidx += 1
					if html:
						print '</tr>'
					elif csv:
						sys.stdout.write('\n')
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
				elif csv:
					sys.stdout.write('%s' % prevdatefmt)
				else:
					sys.stdout.write('%s |' % prevdatefmt)
				colidx = 0
				rowidx = 0
				for value in values:
					if colidx >= max_cols_per_row:
						rowidx += 1
						if html:
							print '</tr><tr class="ca_tr ca_tr_' + oddeven + str(rowidx+1) + '"><td class="ca_td ca_td_' + oddeven + 'date' + str(rowidx+1) + '"></td>'
						elif csv:
							sys.stdout.write('\n,')
						else:
							sys.stdout.write('\n' + ' ' * len(prevdatefmt) + ' |')
						colidx = 0
					if len(value['page']) > 0:
						if html:
							print '<td class="ca_td ca_td_' + oddeven + 'page' + str(rowidx+1) + '">%02d' % int(value['page'])
							if show_deviations:								
								print '<br /><span class="ca_span_deviation">' + time.strftime(time_format, value['time']) + '</span>' 
							print '</td>'
						elif csv:
							sys.stdout.write(',%d' % int(value['page']))
						else:
							sys.stdout.write((' %02d' % int(value['page'])) + (' ' * (len(headers[colidx]) - 2)))
					else:
						dst_start_tm = time.strptime(prevdatestr, '%Y-%m-%d')
						if html:
							print '<td class="ca_td ca_td_' + oddeven + 'page' + str(rowidx+1) + '"></td>'
						if csv:
							sys.stdout.write(',')
						else:
							sys.stdout.write(' ' + (' ' * len(headers[colidx])))
					colidx += 1
				if html:
					print '</tr>'
				elif csv:
					sys.stdout.write('\n')
				else:
					sys.stdout.write('\n')
				if oddeven == 'odd': 
					oddeven = 'even'
				else: 
					oddeven = 'odd'
				values = []
			if not got_headers and not time_indices.has_key(timestr):
				headers.append(time.strftime(header_time_format, tm))
				time_indices[timestr] = len(headers) - 1
			time_index = time_indices[timestr]
			while len(values) <= time_index:
				values.append({'page': ''})
			if len(values[time_index]['page']) > 0:
				dst_end_tm = tm
			values[time_index] = {'page':page, 'time':time.localtime(time.mktime((tm[0],tm[1],tm[2],tm[3],tm[4],tm[5]+int(deviation*60.0),tm[6],tm[7],tm[8]))) }
			found_first_day = True
			prevdatestr = datestr		
	line = sys.stdin.readline()
	
if html:
	if dst_start_tm != None:
		print '<tr><td colspan="25" class="ca_td_dst">times after 0200 on ' + time.strftime('%A, %B %d', dst_start_tm) + ' are adjusted for daylight savings</td></tr>'
	elif dst_end_tm != None:
		print '<tr><td colspan="25" class="ca_td_dst">times until 0200 on ' + time.strftime('%A, %B %d', dst_end_tm) + ' are adjusted for daylight savings</td></tr>'
	elif table_start_tm[1] >= 4 and table_start_tm[1] <= 10:
		print '<tr><td colspan="25" class="ca_td_dst">times are adjusted for daylight savings</td></tr>'		
	print '</table>'
