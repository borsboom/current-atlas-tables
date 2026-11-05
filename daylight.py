# Copyright (c) 2009-2019 Emanuel Borsboom.  See COPYING.txt for license.
#
# Daylight saving time helpers for the table scripts, based on the system
# time zone (TZ) rules rather than fixed dates, so the tables follow changes
# such as British Columbia's move to permanent daylight time (UTC-7) after
# the 2026-03-08 spring forward.
#
# A time counts as daylight time when its UTC offset is ahead of Pacific
# Standard Time.  The offset is used rather than tm_isdst because the time
# zone database labels B.C.'s permanent UTC-7 as standard time (MST).

import calendar
import time

STANDARD_UTC_OFFSET = -8 * 60 * 60 # Pacific Standard Time

def utc_offset(t):
	return calendar.timegm(time.localtime(t)) - int(t)

def is_daylight(t):
	return utc_offset(t) > STANDARD_UTC_OFFSET

def format_utc_offset(t):
	hours = utc_offset(t) / 3600.0
	if hours == int(hours):
		hours = int(hours)
	if hours < 0:
		return 'UTC&minus;' + str(-hours)
	return 'UTC+' + str(hours)

def year_changes(year):
	"""Returns whether the year starts in daylight time, and a list of
	(time, is_daylight) for each change during the year, where time is the
	first whole hour after the change."""
	t = time.mktime((year,1,1,0,0,0,0,0,-1))
	end = time.mktime((year+1,1,1,0,0,0,0,0,-1))
	starts_daylight = prev = is_daylight(t)
	changes = []
	while t < end:
		t += 60 * 60
		cur = is_daylight(t)
		if cur != prev:
			changes.append((t, cur))
			prev = cur
	return starts_daylight, changes

def describe_year(year):
	"""A sentence for the year's tables saying which times are adjusted for
	daylight savings."""
	starts_daylight, changes = year_changes(year)
	kinds = [daylight for (t, daylight) in changes]
	if not starts_daylight and kinds == [True, False]:
		return ('Times <strong>are</strong> adjusted for daylight savings (PDT, 0200 second Sunday '
		        'in March through 0200 first Sunday in November).')
	if not starts_daylight and kinds == [True]:
		t = changes[0][0]
		return ('Times <strong>are</strong> adjusted for daylight savings from 0200 on ' +
		        time.strftime('%A, %B %d', time.localtime(t)) +
		        ', and there is no change back to standard time in November: times stay ' +
		        format_utc_offset(t) + ' through the end of the year.')
	if starts_daylight and kinds == []:
		return ('Times <strong>are</strong> adjusted for daylight savings all year (' +
		        format_utc_offset(time.mktime((year,1,1,0,0,0,0,0,-1))) +
		        '): there are no clock changes.')
	if not starts_daylight and kinds == []:
		return ('Times are standard time all year (' +
		        format_utc_offset(time.mktime((year,1,1,0,0,0,0,0,-1))) +
		        '): there are no clock changes.')
	return ('Clocks change at ' +
	        ' and '.join(['0200 on ' + time.strftime('%A, %B %d', time.localtime(t)) +
	                      ' (to ' + format_utc_offset(t) + ')' for (t, daylight) in changes]) +
	        '; times in the tables follow these changes.')
