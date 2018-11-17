#!/usr/bin/env bash

set -e

if [ $# -ne 5 ]; then
    echo "Usage: sh 02_fetch_surveys.sh <user> <echo-mobile-root> <echo-mobile-username> <echo-mobile-password> <data-root>"
    echo "Downloads all  surveys."
    exit
fi

USER=$1
EM_DIR=$2
EM_USERNAME=$3
EM_PASSWORD=$4
DATA_DIR=$5

ORG="AVF - KEEP II"
VERBOSE="-v"

cd "$EM_DIR"

SURVEYS=(
    "Advert (Mohamed)"
    "Advert(Zamzam)"
    "Adverts"
    "Dadaab Demog Survey_Somali"

    "Dadaab follow up survey (Aisha-mar)"
    "Dadaab follow up survey(Amina-Edu)"
    "Dadaab follow up survey(Mohamed-ed)"
    "Dadaab follow up survey(Zamzam Cho)"
    )

for SURVEY in "${SURVEYS[@]}"
do
    echo "pipenv run python survey_report.py" "$VERBOSE" "$USER" "$EM_USERNAME" "$EM_PASSWORD" "\"$ORG\"" \
        "\"$SURVEY\"" "\"$DATA_DIR/00 UUIDs/phone_uuids.json\"" "\"$DATA_DIR/02 Raw Surveys/$SURVEY.json\""

    pipenv run python survey_report.py "$VERBOSE" "$USER" "$EM_USERNAME" "$EM_PASSWORD" "$ORG" \
        "$SURVEY" "$DATA_DIR/00 UUIDs/phone_uuids.json" "$DATA_DIR/02 Raw Surveys/$SURVEY.json"
done
