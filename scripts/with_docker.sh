#!/usr/bin/env bash
set -eu -o pipefail
cd "$(dirname "$0")/.."
docker build -t borsboom/current-atlas-tables .
docker run --rm -v "$PWD/output:/current-atlas-tables/output" ${DOCKER_RUN_ARGS:-} borsboom/current-atlas-tables "$@"
