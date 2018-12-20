#!/usr/bin/env bash

set -e

if [ $# -ne 2 ]; then
    echo "Usage: sh 05_id_messages.sh <user> <data-root>"
    echo "Computes and applies an ID for each message"
    exit
fi

USER=$1
DATA_DIR=$2

ORG="AVF - KEEP II"

cd ../id_messages

mkdir -p "$DATA_DIR/05 Messages with ID"

SHOWS=(
    "Amina"
    "Aisha"
    "Mohamed"
    "Zamzam"
    )

for SHOW in "${SHOWS[@]}"
do
    echo "sh docker-run.sh" "$USER" "$DATA_DIR/04 Clean Messages/${SHOW}_clean.json" \
        "$DATA_DIR/05 Messages with ID/${SHOW}_with_id.json"

    bash docker-run.sh "$USER" "$DATA_DIR/04 Clean Messages/${SHOW}_clean.json" \
        "$DATA_DIR/05 Messages with ID/${SHOW}_with_id.json"
done
