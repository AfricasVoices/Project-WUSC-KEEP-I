#!/bin/bash

set -e

if [ $# -ne 4 ]; then
    echo "Usage: sh docker-run.sh <user> <input-file> <variable_name> <output-file>"
    exit
fi

USER=$1
INPUT_JSON=$2
VARIABLE_NAME=$3
OUTPUT_JSON=$4

# Build an image for this project, called "wusc-keep-demogs-export-to-coda2".
docker build -t wusc-keep-demogs-export-to-coda2 .

# Create a container from the image that was just built.
container="$(docker container create --env USER="$USER" --env VARIABLE_NAME="$VARIABLE_NAME" wusc-keep-demogs-export-to-coda2)"

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
