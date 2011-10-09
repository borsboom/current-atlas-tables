#!/bin/sh
rsync -vz --progress --rsh=ssh ../output/*.{html,pdf,jpg} epiphyte.ca:/var/www/html/dl/current_atlas_tables/tables/
