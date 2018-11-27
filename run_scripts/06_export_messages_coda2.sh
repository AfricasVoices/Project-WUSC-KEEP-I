#!/usr/bin/env bash

set -e

if [ $# -ne 2 ]; then
    echo "Usage: sh 06_export_messages_to_coda2.sh <user> <data-root>"
    echo "Exports messages to Coda2 for labelling"
    exit
fi

USER=$1
DATA_DIR=$2

ORG="AVF - KEEP II"

cd ../export_messages_to_coda2

mkdir -p "$DATA_DIR/06 Messages For Coda2"

SHOWS=(
    "Amina"
    "Aisha"
    "Mohamed"
    "Zamzam"
    )

for SHOW in "${SHOWS[@]}"
do
    echo "sh docker-run.sh" "$USER" "$DATA_DIR/05 Messages with ID/${SHOW}_with_id.json" \
        "$DATA_DIR/06 Messages For Coda2/${SHOW}_messages_for_Coda2.json"

    sh docker-run.sh "$USER" "$DATA_DIR/05 Messages with ID/${SHOW}_with_id.json" \
        "$DATA_DIR/06 Messages For Coda2/${SHOW}_messages_for_Coda2.json"
done
