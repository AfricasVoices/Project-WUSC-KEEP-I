#!/usr/bin/env bash

set -e

if [ $# -ne 2 ]; then
    echo "Usage: sh 04_clean_messages.sh <user> <data-root>"
    echo "Cleans radio show answers, and exports to CSVs for analysis."
    exit
fi

USER=$1
DATA_DIR=$2

ORG="AVF - KEEP II"

cd ../clean_messages

mkdir -p "$DATA_DIR/04 Clean Messages"

SHOWS=(
    "Amina"
    "Aisha"
    "Mohamed"
    "Zamzam"
    )

for SHOW in "${SHOWS[@]}"
do
    echo "sh docker-run.sh" "$USER" "$DATA_DIR/03 Messages Merged/${SHOW}_merged.json" \
        "$DATA_DIR/04 Clean Messages/${SHOW}_clean.json"

    sh docker-run.sh "$USER" "$DATA_DIR/03 Messages Merged/${SHOW}_merged.json" \
        "$DATA_DIR/04 Clean Messages/${SHOW}_clean.json"
done
