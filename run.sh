#!/bin/bash

set -e
set -o pipefail

DEPLOY_PLACE=$1

# replace ********
export DOCKER_USER=********
export IMAGE=pshs
export TAG=********
export SSH_PEM=********

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
if [ "$DEPLOY_PLACE" = "local" ]; 
    then
        docker compose up -d
    else
        deploy/deploy.sh $DEPLOY_PLACE
fi

exit 0
