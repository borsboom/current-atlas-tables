#!/usr/bin/env bash
set -xeu -o pipefail
cd "$(dirname "$0")/.."
cp current_atlas.jpg output
for year in 2009 2010 2011 2012 2013 2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025 2026 2026 2027 2028 2029 2030; do
  ./year_html.py $year >output/current_atlas_jdf_sog_tables_$year.html
  wkhtmltopdf --page-size Letter --print-media-type output/current_atlas_jdf_sog_tables_$year.html output/current_atlas_jdf_sog_tables_$year.pdf
done
