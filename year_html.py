#!/usr/bin/python
#
# Copyright (c) 2009 Emanuel Borsboom.  See COPYING.txt for license.
#
# Produce formatted HTML for the tables for the year specified on the 
# command-line.
#
# Usage example:
#
#    ./year_html 2009 >2009.html
#

import sys
import time
import posix

year = int(sys.argv[1])

print '<html><head><title>Current Atlas JDF to SOG Tables &mdash; ' + str(year) + '</title>'
print '''
<style type="text/css" media="all">
body { font-family: sans-serif }
.ca_table { border-spacing: 0px; empty-cells: show; background-color: white; font-size: small }
.ca_td { white-space: nowrap }
.ca_td_headerdate1, .ca_td_headerdate2 { background-color: white }
.ca_td_headertime1, .ca_td_headertime2, .ca_td_odddate1, .ca_td_odddate2 { background-color: #77ddff }
.ca_td_evendate1, .ca_td_evendate2 { background-color: #66ccee }
.ca_td_evendate1, .ca_td_evendate2, .ca_td_odddate1, .ca_td_odddate2 { text-align: right }
.ca_td_headertime1, .ca_td_headertime2 { padding-left: 2px; padding-right: 2px }
.ca_td_headertime2 { font-weight: bold }
.ca_td_headerdate2, .ca_td_headertime2 { ; border-bottom: 1px solid black }
.ca_tr_even1, .ca_tr_even2 { background-color: #eeeeee }
.ca_td_evenpage2, .ca_td_oddpage2 { font-weight: bold }
.ca_td_headertime1, .ca_td_headertime2, .ca_td_evenpage1, .ca_td_evenpage2, .ca_td_oddpage1, .ca_td_oddpage2 { text-align: center }
.ca_td_headerdate1, .ca_td_headerdate2, .ca_td_evendate1, .ca_td_evendate2, .ca_td_odddate1, .ca_td_odddate2 { border-right: 1px solid black }
.ca_td_evendate1, .ca_td_evendate2, .ca_td_odddate1, .ca_td_odddate2 { padding-right: 2px }
</style>
<style type="text/css" media="print">
p, li { font-size: 15pt }
a { text-decoration: none; color: black }
.contents { display: none }
</style>
'''
print '</head><body>'
print '<h1 style="text-align:center">Current Atlas JDF to SOG Tables</h1>'
print '<h1 style="text-align:center">' + str(year) + '</h1>'
print '''
<p>&nbsp;</p>
<p style="text-align: center"><em>For use with:
<br />&nbsp;
<br /><strong>Current Atlas / Atlas des Courants</strong>
<br />Juan de Fuca Strait to/&agrave; Strait of Georgia</em>
<br />(Published by the Canadian Hydrographic Service)</p>
<p>&nbsp;</p>
<p>To find the chart number for a date and time, 
find the row for the required date, then read across to the
column closest to the required time, and turn to the chart number shown.
Bold face numbers are for <strong>PM</strong>, regular type is for AM.</p>
<p><strong>These tables are for non-commercial use only!</strong></p>
<p>&nbsp;</p>
<div class="contents"><h4>Contents</h4><ul>
'''
for month in range(1,13):
	print ('<li><a href="#' + ('%02d' % month) + '">' +
	       time.strftime('%B, %Y', time.localtime(time.mktime((year,month,1,0,0,0,0,0,0)))) +
	       '</a></li>')
print '</ul><p>&nbsp;</p></div>'

print '''
<p style="text-align:right"><em>Produced by <strong>Emanuel Borsboom</strong>
<br />Site 11 Comp 9, Mayne Island, B.C.  V0N 2J0
<br /><a href="http://www.epiphyte.ca/code/currents.html">http://www.epiphyte.ca/code/currents.html</a></em></p>

<p style="page-break-before:always">&nbsp;</p>
'''

for month in range(1,13):
	print ('<h3 style="page-break-before:always"><a name="' + ('%02d' % month) + '" />' + 
    	   time.strftime('%B, %Y', time.localtime(time.mktime((year,month,1,0,0,0,0,0,0)))) +
	       '<span style="float:right">Current Atlas JDF to SOG Table</span>' +
	       '</h3>') 
	sys.stdout.flush()
	posix.system('tide -l "Point Atkinson, British Columbia" -f c -b "' +
			     time.strftime('%Y-%m-%d %H:%M', time.localtime(time.mktime((year,month,0,12,0,0,0,0,0)))) +
			     '" -e "' +
			     time.strftime('%Y-%m-%d %H:%M', time.localtime(time.mktime((year,month+1,1,12,0,0,0,0,0)))) +
			     '" | ./calculate.py --time-interval 30 | ./format.py --html --date-format "%a %d"')
			
print '</body></html>'