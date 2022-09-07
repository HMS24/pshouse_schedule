#!/bin/bash

set -xe
set -o pipefail

REMOTE_MACHINE=$1@$2
SSH_PEM="~/chimei_24.pem"

echo "$SCHEDULE_IMAGE" > /tmp/.auth
echo "$SCHEDULE_IMAGE_TAG" >> /tmp/.auth
echo "$DOCKER_USER" >> /tmp/.auth
cat ~/docker_pass >> /tmp/.auth

scp -i $SSH_PEM /tmp/.auth $REMOTE_MACHINE:/tmp/.auth
scp -i $SSH_PEM ./deploy/publish.sh $REMOTE_MACHINE:/tmp/publish.sh
scp -i $SSH_PEM ./compose.yml $REMOTE_MACHINE:~/pshs/compose.yml

ssh -i $SSH_PEM $REMOTE_MACHINE ". /tmp/publish.sh"

exit 0