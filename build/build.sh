#!/bin/bash

set -e

: ${GALAXY_DOCKER_IMAGE:="quay.io/bgruening/galaxy:18.01"}
: ${GALAXY_PORT:="8080"}
: ${EPHEMERIS_VERSION:="0.8.0"}
: ${GALAXY_DEFAULT_ADMIN_USER:="admin@galaxy.org"}
: ${GALAXY_DEFAULT_ADMIN_PASSWORD:="admin"}
: ${EXPORT_DIR:="$HOME/export"}
: ${DATA_MANAGER_DATA_PATH:="${EXPORT_DIR}/data_manager"}

: ${PLANEMO_PROFILE_NAME:="wxflowtest"}
: ${PLANEMO_SERVE_DATABASE_TYPE:="postgres"}

GALAXY_URL="http://localhost:$GALAXY_PORT"

if [ ! -f .venv ]; then
    virtualenv .venv
    . .venv/bin/activate
    pip install -U pip
    #pip install ephemeris=="${EPHEMERIS_VERSION}"
    pip install -e git+https//github.com/galaxyproject/ephemeris.git@dm#egg=ephemeris
fi

. .eph/bin/activate


docker run -it -v /Users/frcop/tmp/docker/export:/export/ -e GALAXY_CONFIG_GALAXY_DATA_MANAGER_DATA_PATH=/export/data_manager/ -p 8080:80 "quay.io/bgruening/galaxy:18.01"
galaxy-wait -g ${GALAXY_URL}

shed-tools install -d genome_data_manager.yaml -g $GALAXY_URL -u $GALAXY_DEFAULT_ADMIN_USER -p $GALAXY_DEFAULT_ADMIN_PASSWORD
run-data-managers --config /Users/frcop/tmp/docker/export/data-managers/inputfile_subset.yaml -g $GALAXY_URL -u $GALAXY_DEFAULT_ADMIN_USER -p $GALAXY_DEFAULT_ADMIN_PASSWORD
