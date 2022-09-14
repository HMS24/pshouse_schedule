#!/bin/bash

set -xe
set -o pipefail

# login
docker login -u $DOCKER_USER --password-stdin < ~/docker_pass

# tag
docker tag $IMAGE:$TAG $DOCKER_USER/$IMAGE:$TAG

# push
docker push $DOCKER_USER/$IMAGE:$TAG

exit 0
