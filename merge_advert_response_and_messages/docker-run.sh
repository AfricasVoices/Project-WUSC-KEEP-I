#!/bin/bash

set -e

if [ $# -ne 5 ]; then
    echo "Usage: sh docker-run.sh <user> <input-file-messages> <group-name> <input-file-adverts-responses> <output-file>"
    exit
fi

USER=$1
INPUT_JSON_MESSAGES=$2
GROUP=$3
INPUT_JSON_ADVERTS=$4
OUTPUT_JSON=$5

# Build an image for this project, called "wusc-keep-merge-messages".
docker build -t wusc-keep-merge-messages .

# Create a container from the image that was just built.
container="$(docker container create --env USER="$USER" --env GROUP="$GROUP" wusc-keep-merge-messages)"

function finish {
    # Tear down the container when done.
    docker container rm "$container" >/dev/null
}
trap finish EXIT

# Copy input data into the container
docker cp "$INPUT_JSON_MESSAGES" "$container:/app/data/input_messages.json"
docker cp "$INPUT_JSON_ADVERTS" "$container:/app/data/input_adverts.json"

# Run the image as a container.
docker start -a -i "$container"

# Copy the output data back out of the container
docker cp "$container:/app/data/output.json" "$OUTPUT_JSON"
