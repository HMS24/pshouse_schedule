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

# deliver history data
echo "**********************************"
echo "** Deliver history data***********"
echo "**********************************"

# scp -i $SSH_PEM ./results/20211001_F_lvr_land_B.csv $DEPLOY_PLACE:~/pshs/results/20211001_F_lvr_land_B.csv
# scp -i $SSH_PEM ./results/20220101_F_lvr_land_B.csv $DEPLOY_PLACE:~/pshs/results/20220101_F_lvr_land_B.csv
# scp -i $SSH_PEM ./results/20220401_F_lvr_land_B.csv $DEPLOY_PLACE:~/pshs/results/20220401_F_lvr_land_B.csv
# scp -i $SSH_PEM ./results/20220601_F_lvr_land_B.csv $DEPLOY_PLACE:~/pshs/results/20220601_F_lvr_land_B.csv
# scp -i $SSH_PEM ./results/20220701_F_lvr_land_B.csv $DEPLOY_PLACE:~/pshs/results/20220701_F_lvr_land_B.csv
# scp -i $SSH_PEM ./results/20220711_F_lvr_land_B.csv $DEPLOY_PLACE:~/pshs/results/20220711_F_lvr_land_B.csv
# scp -i $SSH_PEM ./results/20220721_F_lvr_land_B.csv $DEPLOY_PLACE:~/pshs/results/20220721_F_lvr_land_B.csv
# scp -i $SSH_PEM ./results/20220801_F_lvr_land_B.csv $DEPLOY_PLACE:~/pshs/results/20220801_F_lvr_land_B.csv
# scp -i $SSH_PEM ./results/20220811_F_lvr_land_B.csv $DEPLOY_PLACE:~/pshs/results/20220811_F_lvr_land_B.csv
# scp -i $SSH_PEM ./results/20220821_F_lvr_land_B.csv $DEPLOY_PLACE:~/pshs/results/20220821_F_lvr_land_B.csv
# scp -i $SSH_PEM ./results/20220901_F_lvr_land_B.csv $DEPLOY_PLACE:~/pshs/results/20220901_F_lvr_land_B.csv
# scp -i $SSH_PEM ./results/20220911_F_lvr_land_B.csv $DEPLOY_PLACE:~/pshs/results/20220911_F_lvr_land_B.csv

# truncate database and insert history data!!!!
ssh -i $SSH_PEM $DEPLOY_PLACE "docker exec --workdir /home/admin schedule venv/bin/python3 app.py init"
exit 0
