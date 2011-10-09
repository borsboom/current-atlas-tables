#!/bin/sh
cd ..
cp current_atlas.jpg output
for x in 2011 2012 2013 2014 2015 2016 2017 2018 2019 2020
#for x in 2021 2022 2023 2024 2025 2026 2026 2027 2028 2029 2030
do ./year_html.py $x >output/current_atlas_jdf_sog_tables_$x.html
done
