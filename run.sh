#!/bin/bash -e

set -o pipefail

# declare
TARGET=""
SSH_PEM=""
DOCKER_USER="local"
DOCKER_PASS=""
IMAGE="pshs"
TAG="latest"

# init database default false
INIT=0

while [[ "$#" -gt 0 ]]; do
	case $1 in
		--target) TARGET="$2"; shift ;;
		--ssh-pem) SSH_PEM="$2"; shift ;;
		--docker-user) DOCKER_USER="$2"; shift ;;
		--docker-pass) DOCKER_PASS="$2"; shift ;;
		--image) IMAGE="$2"; shift ;;
		--tag) TAG="$2"; shift ;;
		--init) INIT="$2"; shift ;;
		*) echo "Unknown parameter passed: $1"; exit 1 ;;
	esac
	shift
done

if [ -z "$TARGET" ]; then
	echo "--target argument is required!"
	exit 1
fi

if [ "$TARGET" != "local" ] && [ -z "$SSH_PEM" ]; then
	echo "--ssh-pem argument is required!"
	exit 1
fi

if [ "$TARGET" != "local" ] && [ "$DOCKER_USER" == "local" ]; then
	echo "--docker-user argument is required!"
	exit 1
fi

if [ "$TARGET" != "local" ] && [ -z "$DOCKER_PASS" ]; then
	echo "--docker-pass argument is required!"
	exit 1
fi

# build
echo "**********************************"
echo "** Building image ****************"
echo "**********************************"

build/build.sh $IMAGE $TAG

# test
echo "**********************************"
echo "** Testing ***********************"
echo "**********************************"

build/test.sh $IMAGE $TAG

# push
echo "**********************************"
echo "** Pushing image *****************"
echo "**********************************"

build/push.sh $TARGET $IMAGE $TAG $DOCKER_USER $DOCKER_PASS

# deploy
echo "**********************************"
echo "** Deploying *********************"
echo "**********************************"

echo "Deploy to $TARGET"

if [ "$TARGET" = "local" ]; then
	if docker network ls | grep -Fq "backend_net"; then
        true
    else
        docker network create backend_net -d bridge
	fi

	DOCKER_USER=$DOCKER_USER \
	IMAGE=$IMAGE \
	TAG=$TAG \
	docker compose up -d

else
    deploy/deploy.sh $TARGET $SSH_PEM $IMAGE $TAG $DOCKER_USER $DOCKER_PASS
fi

# insert history data
echo "**********************************"
echo "** Insert history data ***********"
echo "**********************************"

RESULTS_DIR="results"

for file in "$PWD/$RESULTS_DIR"/*.csv
	do
        scp -i $SSH_PEM "$file" $TARGET:~/pshs/"$RESULTS_DIR/$(basename -- $file)"
	done

if [ "$INIT" -eq 1 ]; then
    echo "** Truncate table and insert history data!!!! ***********"

    ssh -i $SSH_PEM $TARGET "docker exec --workdir /home/admin schedule venv/bin/python3 app.py init"
fi

exit 0
