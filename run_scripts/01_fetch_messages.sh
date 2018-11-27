#!/usr/bin/env bash

set -e

if [ $# -ne 5 ]; then
    echo "Usage: sh 01_fetch_messages.sh <user> <echo-mobile-root> <echo-mobile-username> <echo-mobile-password> <data-root>"
    echo "Downloads all radio show answers from all shows."
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

SHOWS=(
    # Start time                Cut-off time                Group name
    "2018-10-19T00:00:00+03:00" "2018-10-24T23:59:00+03:00" "AMINA"
    "2018-10-25T00:00:00+03:00" "2018-10-31T23:59:00+03:00" "AISHA"
    "2018-11-01T00:00:00+03:00" "2018-11-07T23:59:00+03:00" "MOHAMED"
    "2018-11-08T00:00:00+03:00" "2018-11-14T23:59:00+03:00" "ZAMZAM"
    )

for i in $(seq 0 $((${#SHOWS[@]} / 3 - 1))) # for i in range(0, len(SHOWS) / 3)
do
    START_TIME="${SHOWS[3 * i]}"
    END_TIME="${SHOWS[3 * i + 1]}"
    SHOW_NAME="${SHOWS[3 * i + 2]}"

    echo "pipenv run python messages_report.py" "$VERBOSE" "$USER" "$EM_USERNAME" "$EM_PASSWORD" "\"$ORG\"" \
        "$START_TIME" "$END_TIME" "\"$DATA_DIR/00 UUIDs/phone_uuids.json\"" \
        "\"$DATA_DIR/00 UUIDs/message_uuids.json\"" "\"$DATA_DIR/01 Raw Messages/$SHOW_NAME.json\""

    pipenv run python messages_report.py "$VERBOSE" "$USER" "$EM_USERNAME" "$EM_PASSWORD" "$ORG" \
        "$START_TIME" "$END_TIME" "$DATA_DIR/00 UUIDs/phone_uuids.json" \
        "$DATA_DIR/00 UUIDS/message_uuids.json" "$DATA_DIR/01 Raw Messages/$SHOW_NAME.json"
done
