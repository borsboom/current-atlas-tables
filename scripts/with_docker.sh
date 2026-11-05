#!/usr/bin/env bash
set -eu -o pipefail
cd "$(dirname "$0")/.."
# wkhtmltox is packaged for amd64 only, so build and run amd64 on any host
docker build --platform linux/amd64 -t borsboom/current-atlas-tables .
docker run --rm --platform linux/amd64 -v "$PWD/output:/current-atlas-tables/output" ${DOCKER_RUN_ARGS:-} borsboom/current-atlas-tables "$@"
