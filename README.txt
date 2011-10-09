README for Current Atlas Table scripts
-----------------------------------------------------------------------------
Web site: http://www.epiphyte.ca/proj/currents

Copyright (c) 2009-2011 Emanuel Borsboom.  See COPYING.txt for license.

These scripts are used to produce tables of chart numbers for a given 
date/time, to make the current atlas easier to use.  The results are for use
with the _Current Atlas: Juan de Fuca Strait to Strait of Georgia_ 
published by the Canadian Hydrographic Service.  I'm sure these scripts could
be adapted for other CHS current atlases, and I'd be happy to do so if 
one arrives in the mail.

The results should be similar to Murray's Tables or Washburne's tables, but
I've never actually seen them so I'm not sure what other information they
provide.  My reason for writing the script was frustration at the difficulty
of finding stores with these books of tables in stock, especially since
the the data is so easy to calculate.

To use the scripts, you must have xtide (http://www.flaterco.com/xtide/)
installed with the non-free harmonics files ("Restricted-use (non-commercial 
use only) data for locations outside of the U.S.").  Note that since these 
scripts rely on harmonics files which are for non-commercial use only, the 
output of these scripts is under the same restriction.

These scripts have only been tested on a system that is set to the Pacific
time zone.  If your system is configured with a different time zone, the 
results may be unpredictable.  Also only tested on Mac OS X 10.5.7, but I
can't see any reason they wouldn't work on other operating systems.

Here is a summary of the scripts.  See the comments at the top of each script
for more information:

calculate.py
	Takes input from xtide and calculates the chart numbers.  Output is in
	CSV format.
	
format.py
	Formats the output of calculate.py into a text or HTML table.
	
year_html.py
	Generates nicely formatted HTML for a whole year.

