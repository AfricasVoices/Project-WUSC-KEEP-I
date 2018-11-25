#!/usr/bin/env bash

set -e

if [ $# -ne 2 ]; then
    echo "Usage: sh 07_id_surveys.sh <user> <data-root>"
    echo "Computes and applies an ID for each survey response"
    exit
fi

USER=$1
DATA_DIR=$2

ORG="AVF - KEEP II"

cd ../id_surveys

mkdir -p "$DATA_DIR/07 Surveys with ID"

SURVEYS=(
    "Dadaab follow up survey(Amina-Edu)"    "Amina_survey_with_id"
    "Dadaab follow up survey (Aisha-mar)"   "Aisha_survey_with_id"
    "Dadaab follow up survey(Mohamed-ed)"   "Mohamed_survey_with_id"
    "Dadaab follow up survey(Zamzam Cho)"   "Zamzam_survey_with_id"
    )

for i in $(seq 0 $((${#SURVEYS[@]} / 2 - 1)))
do
    INPUT="${SURVEYS[2 * i]}"
    OUTPUT="${SURVEYS[2 * i + 1]}"

    echo "sh docker-run.sh" "$USER" "$DATA_DIR/02 Raw Surveys/${INPUT}.json" \
        "$DATA_DIR/07 Surveys with ID/${OUTPUT}.json"

    sh docker-run.sh "$USER" "$DATA_DIR/02 Raw Surveys/${INPUT}.json" \
        "$DATA_DIR/07 Surveys with ID/${OUTPUT}.json"
done
