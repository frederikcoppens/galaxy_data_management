#!/bin/bash
# based on https://github.com/bgruening/idc/blob/master/run_builder.sh

set -e

: ${GALAXY_DOCKER_IMAGE:="quay.io/bgruening/galaxy:18.01"}
: ${GALAXY_PORT:="8080"}
: ${EPHEMERIS_VERSION:="0.8.0"}
: ${GALAXY_DEFAULT_ADMIN_USER:="admin@galaxy.org"}
: ${GALAXY_DEFAULT_ADMIN_PASSWORD:="admin"}
: ${EXPORT_DIR:="export"}
: ${DATA_MANAGER_DATA_PATH:="${EXPORT_DIR}/data_manager"}

: ${PLANEMO_PROFILE_NAME:="wxflowtest"}
: ${PLANEMO_SERVE_DATABASE_TYPE:="postgres"}

GALAXY_URL="http://localhost:$GALAXY_PORT"

if [ ! -d .venv ]; then
    echo 'installing ephemeris'
    virtualenv .venv
    . .venv/bin/activate
    pip install -U pip
    pip install -e git+https://github.com/galaxyproject/ephemeris.git@dm#egg=ephemeris
fi

echo 'ephemeris installed'

. .venv/bin/activate

mkdir -p ${DATA_MANAGER_DATA_PATH}

if [ ! "$(docker ps | grep 'quay.io/bgruening/galaxy:18.01')" ]; then
  echo "starting docker"
  docker run -d -v ${EXPORT_DIR}:/export/ -e GALAXY_CONFIG_GALAXY_DATA_MANAGER_DATA_PATH=/export/data_manager/ -p 8080:80 "quay.io/bgruening/galaxy:18.01"
fi
galaxy-wait -g ${GALAXY_URL}

shed-tools install -d ../genomes/genome_data_manager.yaml -g $GALAXY_URL -u $GALAXY_DEFAULT_ADMIN_USER -p $GALAXY_DEFAULT_ADMIN_PASSWORD
run-data-managers --config ../genomes/genome_data_manager.yaml -g $GALAXY_URL -u $GALAXY_DEFAULT_ADMIN_USER -p $GALAXY_DEFAULT_ADMIN_PASSWORD
