#!/bin/bash

set -xe
set -o pipefail

# due to permission, as root
docker run --user="root" --rm $IMAGE:$TAG \
    /bin/bash -c "venv/bin/pip3 install -r requirements.test.txt && venv/bin/pytest"

exit 0
