#!/usr/bin/env bash

set -e

if [ $# -ne 2 ]; then
    echo "Usage: sh 08_export_surveys_to_coda2.sh <user> <data-root>"
    echo "Exports surveys to Coda2 for labelling"
    exit
fi

USER=$1
DATA_DIR=$2

ORG="AVF - KEEP II"

cd ../export_surveys_to_coda2

mkdir -p "$DATA_DIR/08 Surveys For Coda2"

SURVEYS=(
    "Amina"
    "Aisha"
    "Mohamed"
    "Zamzam"
    )

VAR_NAMES=(
    "Selected_Empirical_Expectations"
    "Selected_Normative_Expectations"
    "Selected_Parenthood"
    # "Selected_Reference_Groups"
    "Selected_Sanctions"
)

for SURVEY in "${SURVEYS[@]}"
do
    for VAR_NAME in "${VAR_NAMES[@]}"
    do
        echo "sh docker-run.sh" "$USER" "$DATA_DIR/07 Surveys with ID/${SURVEY}_survey_with_id.json" ${VAR_NAME} \
            "$DATA_DIR/08 Surveys For Coda2/${SURVEY}_${VAR_NAME}_survey_for_Coda2.json"

        sh docker-run.sh "$USER" "$DATA_DIR/07 Surveys with ID/${SURVEY}_survey_with_id.json" ${VAR_NAME} \
            "$DATA_DIR/08 Surveys For Coda2/${SURVEY}_${VAR_NAME}_survey_for_Coda2.json"
    done
done
