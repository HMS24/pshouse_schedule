#!/bin/bash

set -xe
set -o pipefail

DOCKERFILE_DIR_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# build docker image
docker buildx build \
--platform linux/amd64 \
-t $SCHEDULE_IMAGE:$SCHEDULE_IMAGE_TAG \
-f $DOCKERFILE_DIR_PATH/Dockerfile .

exit 0
