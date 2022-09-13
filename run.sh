#!/bin/bash

set -e
set -o pipefail

DEPLOY_PLACE=$1

# replace ??????
export DOCKER_USER=?????? && export SCHEDULE_IMAGE=?????? && export SCHEDULE_IMAGE_TAG=??????

if [ -z "$DEPLOY_PLACE" ]; then
	echo "DEPLOY_PLACE argument is required!"
	exit 1
fi

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

echo "Deploy to $DEPLOY_PLACE"
if [ "$USER" = "$DEPLOY_PLACE" ]; 
    then
        docker compose up -d
    else
        deploy/deploy.sh $DEPLOY_PLACE
fi

exit 0
