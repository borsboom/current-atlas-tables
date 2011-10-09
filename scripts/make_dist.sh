#!/bin/sh
rm dist/current_atlas_table_calculator-$1.zip
cd source
zip ../dist/current_atlas_table_calculator-$1.zip *.py *.txt
cd ..
rsync -vz --progress --rsh="ssh -i $HOME/.ssh/nfsn_id_rsa" dist/current_atlas_table_calculator-$1.zip eborsboom_epiphyte@ssh.phx.nearlyfreespeech.net:downloads/current_atlas_tables/source/
ssh -i ~/.ssh/nfsn_id_rsa eborsboom_epiphyte@ssh.phx.nearlyfreespeech.net "rm downloads/current_atlas_tables/source/current_atlas_table_calculator-current.zip; ln -s current_atlas_table_calculator-$1.zip downloads/current_atlas_tables/source/current_atlas_table_calculator-current.zip"
