#!/bin/bash

set -e
set -o pipefail

export IMAGE=$(sed -n '1p' /tmp/.auth)
export TAG=$(sed -n '2p' /tmp/.auth)
export DOCKER_USER=$(sed -n '3p' /tmp/.auth)
DOCKER_PASS=$(sed -n '4p' /tmp/.auth)

rm /tmp/.auth

echo "$DOCKER_PASS" > docker login -u $DOCKER_USER --password-stdin

# In compose to mount volume will occur permission issue, so mkdir results/check dir and debug.log file here.
cd ~/pshs \
&& mkdir -p results/check \
&& touch debug.log

if docker network ls | grep -Fq "backend_net"; then
    true
else
    docker network create backend_net -d bridge
fi

docker compose up -d

exit 0