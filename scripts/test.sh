#!/usr/bin/env bash
set -xeu -o pipefail
cd "$(dirname "$0")/.."
tide -l "Point Atkinson, British Columbia" -f c -z -b '2008-09-30 19:00' -e '2008-10-11 19:00'|./calculate.py|./format.py
