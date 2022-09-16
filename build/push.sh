#!/bin/bash

set -xe
set -o pipefail

TARGET=$1
IMAGE=$2
TAG=$3
DOCKER_USER=$4
DOCKER_PASS=$5

docker tag $IMAGE:$TAG $DOCKER_USER/$IMAGE:$TAG

if [ "$TARGET" = "local" ];
    then
        true
    else
        docker login -u $DOCKER_USER --password-stdin < $DOCKER_PASS
        docker push $DOCKER_USER/$IMAGE:$TAG
fi

exit 0
