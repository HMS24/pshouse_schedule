#!/bin/bash

set -e
set -o pipefail

USER=$1
HOST=$2

# replace ??????
export DOCKER_USER=?????? && export SCHEDULE_IMAGE=?????? && export SCHEDULE_IMAGE_TAG=??????

# build
echo "**********************************"
echo "** Building image ****************"
echo "**********************************"

build/build.sh

# test
echo "**********************************"
echo "** Testing ***********************"
echo "**********************************"

build/test.sh

# push
echo "**********************************"
echo "** Pushing image *****************"
echo "**********************************"

build/push.sh

# deploy
echo "**********************************"
echo "** Deploying *********************"
echo "**********************************"

if [ "$USER" = "localhost" ]; 
    then
        echo "Deploy to localhost"
        docker compose up -d
    else
        echo "Deploy to $USER@$HOST"
        deploy/deploy.sh $USER $HOST
fi

exit 0
