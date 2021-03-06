#!/usr/bin/python
#
# Copyright (c) 2009-2019 Emanuel Borsboom.  See COPYING.txt for license.
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

print '<html><head><title>Current Atlas Lookup Tables: Juan de Fuca Strait to Strait of Georgia &mdash; ' + str(year) + '</title>'
print '''
<style type="text/css" media="all">
body { font-family: sans-serif }
.ca_table { empty-cells: show; background-color: white }
.ca_td { white-space: nowrap }
.ca_td_headerdate1 { background-color: white }
.ca_td_headertime1, .ca_td_odddate1 { background-color: #77ddff }
.ca_td_evendate1 { background-color: #66ccee }
.ca_td_evendate1, .ca_td_odddate1 { text-align: right }
.ca_td_headertime1 { font-weight: bold }
.ca_td_headerdate1, .ca_td_headertime1 { border-bottom: 1px solid black }
.ca_tr_even1 { background-color: #eeeeee }
.ca_td_headertime1 { text-align: center }
.ca_td_headerdate1, .ca_td_evendate1, .ca_td_odddate1 { border-right: 1px solid black }
.ca_td_evendate1, .ca_td_odddate1 { padding-right: 2px; font-weight: bold }
.ca_td_evenpage1, .ca_td_oddpage1 { text-align: center; padding-left:2px; padding-right:2px }
.ca_span_deviation { color: #888888; font-size: small }
.ca_span_dayofweek { font-size: small; font-weight: normal }
.ca_td_dst { font-size: small; text-align:right; font-style: italic }
.printonly { display: none }
</style>
<style type="text/css" media="print">
p, li { font-size: 15pt }
a { text-decoration: none; color: black }
.onlineonly { display: none }
.printonly { display:block }
</style>
'''
print '</head><body>'
print '<h1 style="text-align:center">Current Atlas Lookup Tables</h1>'
print '<h2 style="text-align:center">Juan de Fuca Strait to Strait of Georgia</h2>'
print '<h1 style="text-align:center">' + str(year) + '</h1>'
print '<p style="text-align:center" class="onlineonly"><a href="https://borsboom.io/current-atlas-tables/">Other Years and Printable PDFs</a></p>'
print '''
<p style="text-align: center"><em>For use with:</em>
<br /><img src="current_atlas.jpg" width="431" height="591" style="border: 1px solid black"/>
<!--
<br />&nbsp;
<br /><em>Current Atlas / Atlas des Courants</em>
<br /><em><strong>Juan de Fuca Strait to/&agrave; Strait of Georgia</strong></em>
<br />(Published by the Canadian Hydrographic Service)
-->
</p>
<p>To find the chart number for a date and time,
first find the table for the required date, then find the row for the required day,
then read across to the
column for required hour, and finally turn to the chart number in the <em>Current Atlas</em>.
The small time below the chart number indicates the actual time
that the chart most closely matches.  Times <strong>are</strong> adjusted for daylight savings (PDT, 0200 second Sunday in March through 0200 first Sunday in November).</p>
<p><strong>These tables are for non-commercial use only!</strong></p>
<p>For tables for other years<span class="onlineonly"> and printable PDFs</span>, visit <a href="https://borsboom.io/current-atlas-tables/">borsboom.io/current-atlas-tables</a>.
<div class="onlineonly"><h4>Contents</h4><ul>
'''
for month in range(1,13):
	print ('<li><a href="#' + ('%02d' % month) + '">' +
	       time.strftime('%B, %Y', time.localtime(time.mktime((year,month,1,0,0,0,0,0,0)))) +
	       '</a></li>')
print '</ul></div>'

print '''
<p style="float:right; text-align:right; font-size: small">
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/2.5/ca/"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-nc-sa/2.5/ca/88x31.png" /></a><br /><span xmlns:dc="http://purl.org/dc/elements/1.1/" href="http://purl.org/dc/dcmitype/Text" property="dc:title" rel="dc:type">Licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/2.5/ca/">Creative Commons<br />Attribution-Noncommercial-Share<br />Alike 2.5 Canada License</a>.
</p>
<p style="page-break-after:always">
&nbsp;<br />
<em>Produced by <strong>Emanuel Borsboom</strong>
<br />Mayne Island, B.C.
<br />web: <a href="https://borsboom.io/">borsboom.io</a></em>
</p>
<p class="printonly" style="page-break-after:always;text-align:center">(this page intentionally left blank)</p>
'''

for month in range(1,13):
	print ('<h3 style="margin-bottom:4pt;page-break-before:always"><a name="' + ('%02d' % month) + '" />' + 
    	   time.strftime('%B, %Y', time.localtime(time.mktime((year,month,1,0,0,0,0,0,0)))) +
	       '<span class="printonly" style="float:right;font-size:smaller">Current Atlas Lookup Tables: Juan de Fuca Strait to Strait of Georgia</span>' +
	       '</h3><center>&nbsp;<br />')
	sys.stdout.flush()
	posix.system('tide -l "Point Atkinson, British Columbia" -f c -b "' +
			     time.strftime('%Y-%m-%d %H:%M', time.localtime(time.mktime((year,month,0,12,0,0,0,0,0)))) +
			     '" -e "' +
			     time.strftime('%Y-%m-%d %H:%M', time.localtime(time.mktime((year,month+1,1,12,0,0,0,0,0)))) +
			     '" | ./calculate.py --time-interval 60 | ./format.py --html --header-time-format "%H" --time-format "%H%M" --date-format \'%d<br /><span class="ca_span_dayofweek">%a</span>\' --deviations')
	print '</center>'

print '</body></html>'
