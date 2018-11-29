#!/usr/bin/env bash

set -e

if [ $# -ne 2 ]; then
    echo "Usage: sh 10_export_demogs_to_coda2.sh <user> <data-root>"
    echo "Exports surveys to Coda2 for labelling"
    exit
fi

USER=$1
DATA_DIR=$2

ORG="AVF - KEEP II"

cd ../export_demogs_to_coda2

mkdir -p "$DATA_DIR/10 Demogs For Coda2"

VAR_NAMES=(
    "Selected_Location"
    "Selected_Age"
    "Selected_Gender"
)

for VAR_NAME in "${VAR_NAMES[@]}"
do
    echo "sh docker-run.sh" "$USER" "$DATA_DIR/09 Demogs with ID/Demog_survey_with_id.json" ${VAR_NAME} \
        "$DATA_DIR/10 Demogs For Coda2/Demogs_${VAR_NAME}_survey_for_Coda2.json"

    sh docker-run.sh "$USER" "$DATA_DIR/09 Demogs with ID/Demog_survey_with_id.json" ${VAR_NAME} \
        "$DATA_DIR/10 Demogs For Coda2/Demogs_${VAR_NAME}_survey_for_Coda2.json"
done
