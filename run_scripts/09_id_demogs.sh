#!/usr/bin/env bash

set -e

if [ $# -ne 2 ]; then
    echo "Usage: sh 09_id_demogs.sh <user> <data-root>"
    echo "Computes and applies an ID for each survey response"
    exit
fi

USER=$1
DATA_DIR=$2

ORG="AVF - KEEP II"

cd ../id_demogs

mkdir -p "$DATA_DIR/09 Demogs with ID"

SURVEYS=(
    "Dadaab Demog Survey_Somali"    "Demog_survey_with_id"
    )

for i in $(seq 0 $((${#SURVEYS[@]} / 2 - 1)))
do
    INPUT="${SURVEYS[2 * i]}"
    OUTPUT="${SURVEYS[2 * i + 1]}"

    echo "sh docker-run.sh" "$USER" "$DATA_DIR/02 Raw Surveys/${INPUT}.json" \
        "$DATA_DIR/09 Demogs with ID/${OUTPUT}.json"

    sh docker-run.sh "$USER" "$DATA_DIR/02 Raw Surveys/${INPUT}.json" \
        "$DATA_DIR/09 Demogs with ID/${OUTPUT}.json"
done
