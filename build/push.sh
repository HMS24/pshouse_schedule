#!/bin/bash

set -xe
set -o pipefail

# login
docker login -u $DOCKER_USER --password-stdin < ~/docker_pass

# tag
docker tag $SCHEDULE_IMAGE:$SCHEDULE_IMAGE_TAG $DOCKER_USER/$SCHEDULE_IMAGE:$SCHEDULE_IMAGE_TAG

# push
docker push $DOCKER_USER/$SCHEDULE_IMAGE:$SCHEDULE_IMAGE_TAG

exit 0
