#!/usr/bin/env bash
set -xeu -o pipefail
cd "$(dirname "$0")/../output"
for file in *.{html,pdf,jpg}; do
  aws s3 cp --acl=public-read "$file" "s3://downloads.borsboom.io/current-atlas-tables/tables/$file"
done
