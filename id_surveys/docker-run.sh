#!/bin/bash

set -e

if [ $# -ne 3 ]; then
    echo "Usage: sh docker-run.sh <user> <input-file> <output-file>"
    exit
fi

USER=$1
INPUT_JSON=$2
OUTPUT_JSON=$3

# Build an image for this project, called "wusc-keep-surveys-id-applier".
docker build -t wusc-keep-surveys-id-applier .

# Create a container from the image that was just built.
container="$(docker container create --env USER="$USER" wusc-keep-surveys-id-applier)"

function finish {
    # Tear down the container when done.
    docker container rm "$container" >/dev/null
}
trap finish EXIT

# Copy input data into the container
docker cp "$INPUT_JSON" "$container:/app/data/input.json"

# Run the image as a container.
docker start -a -i "$container"

# Copy the output data back out of the container
docker cp "$container:/app/data/output.json" "$OUTPUT_JSON"
